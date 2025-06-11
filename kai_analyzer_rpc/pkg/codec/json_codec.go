package codec

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"reflect"
	"strconv"
	"strings"
	"sync/atomic"
	"time"

	rpc "github.com/cenkalti/rpc2"

	"github.com/go-logr/logr"
)

const headerString = "Content-Length: %d\r\n\r\n"

type Codec interface {
	rpc.Codec
}

type codec struct {
	reader  *bufio.Reader
	writer  *bufio.Writer
	logger  logr.Logger
	scanner *bufio.Scanner

	//temp workspace a new codec is created on every connection
	// This is the workspace to deal with a single connection
	msg              message
	serverRequest    serverRequest
	clientResponse   clientResponse
	isLanguageServer bool

	state *rpc.State
	ctx   context.Context

	notificationServiceName string
}

func NewCodec(ctx context.Context, reader *bufio.Reader, writer *bufio.Writer, logger logr.Logger, notificationServiceName string, state *rpc.State) Codec {
	// Set new seq for this codec/connection
	scanner := bufio.NewScanner(reader)
	c := codec{
		logger:                  logger.WithName("json codec"),
		reader:                  reader,
		scanner:                 scanner,
		writer:                  writer,
		state:                   state,
		ctx:                     ctx,
		notificationServiceName: notificationServiceName,
		isLanguageServer:        true,
	}
	scanner.Split(c.splitLanguageServer)
	return &c
}

//TODO: we need to rewrite the rpc.Client to use the context from here, when calling a handler.
// func (c *codec) setRequestContext(seq uint64, ctx context.Context, cancelFunc func()) {
// 	c.state.Set(fmt.Sprintf("context-%v", seq), ctx)
// 	c.state.Set(fmt.Sprintf("context-cancel-%v", seq), cancelFunc)
// }

func (c *codec) getPending(seq uint64) (*json.RawMessage, bool) {
	if v, ok := c.state.Get(fmt.Sprintf("pending-%v", seq)); ok {
		if m, isCorrectType := v.(*json.RawMessage); isCorrectType {
			return m, true
		}
	}
	return nil, false
}

func (c *codec) getSeq() *atomic.Uint64 {
	if v, ok := c.state.Get("seq"); ok {
		if m, isCorrectType := v.(*atomic.Uint64); isCorrectType {
			return m
		}
	}
	return nil
}

func (c *codec) setPending(a uint64, m *json.RawMessage) {
	c.state.Set(fmt.Sprintf("pending-%v", a), m)
}

func (c *codec) removePending(a uint64) {
	c.state.Set(fmt.Sprintf("pending-%v", a), nil)
}

func (c *codec) ReadHeader(r *rpc.Request, o *rpc.Response) error {
	for !c.scanner.Scan() {
		select {
		case <-c.ctx.Done():
			return io.EOF
		case <-time.After(100 * time.Millisecond):
			continue
		}
	}
	c.logger.V(7).Info("reading request header", "request", r, "body", c.scanner.Text())
	// Need to figure out how to stop this
	// Strip null characters.
	c.msg = message{}
	b := c.scanner.Bytes()
	if len(b) == 0 {
		return io.EOF
	}
	err := json.Unmarshal(b, &c.msg)
	if err != nil {
		c.logger.Error(err, "error unmarshaling body into request/response message", "b", string(b))
		return err
	}
	err = c.handleMessage(r, o)
	c.logger.V(7).Info("finished request header", "err", err, "request", r)
	return nil
}

func (c *codec) handleMessage(r *rpc.Request, o *rpc.Response) error {
	if c.msg.Method != "" {
		// request comes to server
		c.serverRequest.Id = c.msg.Id
		c.serverRequest.Method = c.msg.Method
		c.serverRequest.Params = c.msg.Params

		r.Method = c.serverRequest.Method

		if c.serverRequest.Id != nil {
			b, err := c.serverRequest.Id.MarshalJSON()
			if err != nil {
				c.logger.Error(err, "unable to marshal id")
				return err
			}
			c.logger.Info("b", "b", b)
			i, err := strconv.ParseUint(string(b), 10, 64)
			if err != nil {
				c.logger.Error(err, "unable to parse id")
				return err
			}
			c.serverRequest.unMarshalledId = &i
		}

		if c.serverRequest.unMarshalledId == nil && c.serverRequest.Params == nil {
			params := fmt.Sprintf(`[{"type": "%s"}]`, c.msg.Method)
			m := json.RawMessage(params)
			c.serverRequest.Params = &m
		}

		// JSON request id can be any JSON value;
		// RPC package expects uint64.  Translate to
		// internal uint64 and save JSON on the side.
		c.logger.Info("server request", "server request", c.serverRequest, "notificationService", c.notificationServiceName)
		if c.serverRequest.unMarshalledId == nil && c.notificationServiceName != "" {
			c.serverRequest.Method = c.notificationServiceName
			r.Seq = 0
			r.Method = c.notificationServiceName
		} else {
			s := c.getSeq()
			v := s.Add(1)
			c.setPending(v, c.serverRequest.Id)
			// TODO: enable when the client can use the state, to make pass the context to the handler
			// requestContext, cancelFunc := context.WithCancel(c.ctx)
			// c.setRequestContext(v, requestContext, cancelFunc)
			c.serverRequest.Id = nil
			r.Seq = v
		}
	} else {
		// response comes to client
		err := json.Unmarshal(*c.msg.Id, &c.clientResponse.Id)
		if err != nil {
			return err
		}
		c.clientResponse.Result = c.msg.Result
		c.clientResponse.Error = c.msg.Error

		o.Error = ""
		o.Seq = c.clientResponse.Id
		if c.clientResponse.Error != nil || c.clientResponse.Result == nil {
			x, ok := c.clientResponse.Error.(string)
			if !ok {
				c.logger.Info("unable to get client response as error string", "err", err)
				return nil
			}
			if x == "" {
				x = "unspecified error"
			}
			o.Error = x
		}
	}
	return nil
}

func (c *codec) WriteRequest(r *rpc.Request, v any) error {
	c.logger.V(7).Info("write request", "request", r, "value", v)
	req := &clientRequest{Method: r.Method, JsonRPCVersion: "2.0"}

	// Check if param is a slice of any kind
	if v != nil && reflect.TypeOf(v).Kind() == reflect.Slice {
		// If it's a slice, leave as is
		req.Params = v
	} else {
		// Put anything else into a slice
		req.Params = []interface{}{v}
	}

	if r.Seq == 0 {
		// Notification
		req.Id = nil
	} else {
		seq := r.Seq
		req.Id = &seq
	}
	b, err := json.Marshal(req)
	if err != nil {
		c.logger.V(7).Info("unable to marshal request", "err", err)
		return err
	}
	if c.isLanguageServer {
		n, err := c.writer.Write(([]byte(fmt.Sprintf(headerString, len(b)))))
		if err != nil {
			c.logger.Error(err, "unable to write header string")
			return err
		}
		c.logger.V(7).Info("finished writing language server header", "wrote", n)
	}
	n, err := c.writer.Write(b)
	if err != nil {
		c.logger.Error(err, "unable to write request body")
		return err
	}
	err = c.writer.Flush()
	if err != nil {
		c.logger.Error(err, "unable to flush writer for request")
		return err
	}
	c.logger.V(7).Info("finished writing request", "err", err, "request", r, "wrote", n)
	return nil
}

//var errMissingParams = errors.New("jsonrpc: request body missing params")

func (c *codec) ReadRequestBody(r any) error {
	if r == nil {
		return nil
	}
	c.logger.V(7).Info("read request body", "request", r, "type of r", reflect.TypeOf(r).Kind())

	if c.serverRequest.Params == nil {
		c.logger.Info("here missing params")
		return nil
	}

	var err error

	rt := reflect.TypeOf(r)
	if rt.Kind() == reflect.Ptr && rt.Elem().Kind() == reflect.Slice {
		// If it's a slice, unmarshal as is
		err = json.Unmarshal(*c.serverRequest.Params, r)
	} else {
		// Anything else unmarshal into a slice containing x
		params := &[]interface{}{r}
		err = json.Unmarshal(*c.serverRequest.Params, params)
		if err != nil {
			err = json.Unmarshal(*c.serverRequest.Params, r)
		}
	}
	c.logger.V(7).Info("finished request body", "err", err, "request", r)
	return nil
}

//var null = json.RawMessage([]byte("null"))

func (c *codec) WriteResponse(r *rpc.Response, v any) error {
	c.logger.V(7).Info("writing response", "response", r, "object", v)
	if c.serverRequest.unMarshalledId == nil {
		c.logger.V(7).Info("dont respond on notifications")
		return nil
	}
	b, ok := c.getPending(r.Seq)
	if !ok {
		c.logger.Info("invalid sequence number in response", "number", r.Seq)
		return fmt.Errorf("unable to find pending matching request")
	}
	c.removePending((r.Seq))

	resp := serverResponse{Id: b, JsonRPCVersion: "2.0"}
	if r.Error == "" {
		resp.Result = v
	} else {
		resp.Error = r.Error
	}
	outBytes, err := json.Marshal(resp)
	if err != nil {
		c.logger.V(7).Info("unable to marshall response bytes", "err", err)
		return nil
	}
	if c.isLanguageServer {
		n, err := c.writer.Write(([]byte(fmt.Sprintf(headerString, len(outBytes)))))
		if err != nil {
			c.logger.Info("unable to write header", "err", err)
			return nil
		}
		c.logger.V(7).Info("finished writing language server header", "wrote", n)
	}
	n, err := c.writer.Write(outBytes)
	if err != nil {
		c.logger.Error(err, "unable to write response body")
		return err
	}
	err = c.writer.Flush()
	if err != nil {
		c.logger.Error(err, "unable to flush to writer for response")
		return err
	}
	c.logger.V(7).Info("finished write response", "err", err, "bytes", n, "outBytes", string(outBytes))
	return nil
}

func (c *codec) ReadResponseBody(v any) error {
	c.logger.V(7).Info("read response body", "response", v)
	if v == nil {
		return nil
	}
	if c.clientResponse.Result == nil {
		return nil
	}
	b, err := c.clientResponse.Result.MarshalJSON()
	if err != nil {
		return err
	}
	if string(b) == string([]byte("null")) {
		return nil
	}
	err = json.Unmarshal(*c.clientResponse.Result, v)
	c.logger.V(7).Info("finished read response body", "err", err, "body", v)
	return err
}

func (c *codec) Close() error {
	c.logger.Info("Calling Close!!!")
	return nil
}

func (c *codec) splitLanguageServer(data []byte, atEOF bool) (advance int, token []byte, err error) {
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}
	// Find any headers
	if i := bytes.Index(data, []byte("\r\n\r\n")); i >= 0 {
		readContentHeader := data[0:i]
		c.logger.V(7).Info("found header", "header", fmt.Sprintf("%q", readContentHeader))
		if !strings.Contains(string(readContentHeader), "Content-Length") {
			return 0, nil, fmt.Errorf("found header separator but not content-length header")
		}
		pieces := strings.Split(string(readContentHeader), ":")
		if len(pieces) != 2 {
			return 0, nil, fmt.Errorf("invalid pieces")
		}
		addedLength, err := strconv.Atoi(strings.TrimSpace(pieces[1]))
		if err != nil {
			return 0, nil, err
		}
		if i+4+addedLength > len(data) {
			// wait for the buffer to fill up
			c.logger.Info("here - waiting for more data from buffer in scanner")
			return 0, nil, nil
		}
		return i + addedLength + 4, data[i+4 : i+4+addedLength], nil
	}
	if atEOF {
		c.logger.V(7).Info("scanner at EOF")
		return len(data), data, nil
	}
	return 0, nil, nil
}
