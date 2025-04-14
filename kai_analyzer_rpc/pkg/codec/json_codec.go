package codec

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"reflect"
	"strconv"
	"strings"
	"sync"

	rpc "github.com/cenkalti/rpc2"

	"github.com/go-logr/logr"
)

const headerString = "Content-Length: %d\r\n\r\n"

type Codec interface {
	rpc.Codec
}

type codec struct {
	connection io.ReadWriteCloser
	reader     *bufio.Reader
	writer     *bufio.Writer
	logger     logr.Logger

	//temp workspace a new codec is created on every connection
	// This is the workspace to deal with a single conection
	msg              message
	serverRequest    serverRequest
	clientResponse   clientResponse
	isLanguageServer bool

	mutex   sync.Mutex
	pending map[uint64]*json.RawMessage
	seq     uint64

	notificationServiceName string
}

func NewCodec(connection io.ReadWriteCloser, logger logr.Logger, notificationSericeName string) Codec {
	return &codec{
		logger:                  logger.WithName("json codec"),
		connection:              connection,
		reader:                  bufio.NewReader(connection),
		writer:                  bufio.NewWriter(connection),
		pending:                 make(map[uint64]*json.RawMessage),
		mutex:                   sync.Mutex{},
		notificationServiceName: notificationSericeName,
		isLanguageServer:        true,
	}
}
func (c *codec) splitLanguageServer(data []byte, atEOF bool) (advance int, token []byte, err error) {
	c.logger.Info("data", fmt.Sprintf("%q", data))
	if atEOF && len(data) == 0 {
		return 0, nil, nil
	}
	// Find any headers
	if i := bytes.Index(data, []byte("\r\n\r\n")); i >= 0 {
		readContentHeader := data[0:i]
		c.logger.Info("found header", "hearder", fmt.Sprintf("%q", readContentHeader))
		if !strings.Contains(string(readContentHeader), "Content-Length") {
			c.logger.Info("here - content-length")
			return 0, nil, fmt.Errorf("found header seperator but not content-length header")
		}
		pieces := strings.Split(string(readContentHeader), ":")
		c.logger.Info("pieces", "p", pieces)
		if len(pieces) != 2 {
			c.logger.Info("here - pieces")
			return 0, nil, fmt.Errorf("invalid pieces")
		}
		addedLength, err := strconv.Atoi(strings.TrimSpace(pieces[1]))
		if err != nil {
			c.logger.Info("here - addedLength", "err", err)
			return 0, nil, err
		}
		if i+4+addedLength > len(data) {
			// wait for the buffer to fill up
			c.logger.Info("here - waiting for more data from buffer in scanner")
			return 0, nil, nil
		}
		c.logger.Info("return", "v", i+addedLength, "d", fmt.Sprintf("%q", data[i+4:i+4+addedLength]))
		return i + addedLength + 4, data[i+4 : i+4+addedLength], nil
	}
	if atEOF {
		c.logger.Info("at EOF")
		return len(data), data, nil
	}
	return 0, nil, nil
}

func (c *codec) ReadHeader(r *rpc.Request, o *rpc.Response) error {
	defer func() {
		if r := recover(); r != nil {
			c.logger.Info("Recovered in readHeader", "panic", fmt.Sprintf("%v", r))
		}
	}()
	c.logger.V(7).Info("reading request header", "request", r)
	// Need to figure out how to stop this
	scan := bufio.NewScanner(c.reader)
	scan.Split(c.splitLanguageServer)
	couldScan := scan.Scan()
	if !couldScan {
		return nil
	}

	// Strip null characters.
	c.logger.V(7).Info("read request header", "buffer", headerString, "request", r)
	c.logger.V(3).Info("dealing with Language Server Protocol")
	c.isLanguageServer = true
	c.msg = message{}
	err := json.Unmarshal(scan.Bytes(), &c.msg)
	if err != nil {
		c.logger.Info("error unmarshelling body into request/response message", "err", err)
		return nil
	}
	c.logger.Info("read header", "request", r)
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

		b := []byte{}
		c.serverRequest.Id.UnmarshalJSON(b)
		if len(b) == 0 {
			c.serverRequest.unMarshalledId = nil
		} else {
			i, err := strconv.ParseUint(string(b), 10, 64)
			if err != nil {
				c.logger.Info("unable to parse id", "err", err)
				return nil
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
		c.logger.Info("server request", "server request", c.serverRequest, "b", b, "b-string", b, "l", len(b), "notificationService", c.notificationServiceName)
		if len(b) == 0 && c.notificationServiceName != "" {
			c.serverRequest.Method = c.notificationServiceName
			r.Seq = 0
			r.Method = c.notificationServiceName
		} else {
			c.mutex.Lock()
			c.seq++
			c.pending[c.seq] = c.serverRequest.Id
			c.serverRequest.Id = nil
			r.Seq = c.seq
			c.mutex.Unlock()
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
		return nil
	}
	if c.isLanguageServer {
		n, err := c.connection.Write(([]byte(fmt.Sprintf(headerString, len(b)))))
		if err != nil {
			c.logger.Info("unable to write header string", "err", err)
			return err
		}
		c.logger.V(7).Info("finshed writing language server header", "wrote", n)
	}
	n, err := c.connection.Write(b)
	c.logger.V(7).Info("finished writing request", "err", err, "request", r, "wrote", n)
	return nil
}

//var errMissingParams = errors.New("jsonrpc: request body missing params")

func (c *codec) ReadRequestBody(r any) error {
	defer func() {
		if r := recover(); r != nil {
			c.logger.Info("Recovered in readHeader", "panic", fmt.Sprintf("%v", r))
		}
	}()
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
		c.logger.Info("here - slice")
		// If it's a slice, unmarshal as is
		err = json.Unmarshal(*c.serverRequest.Params, r)
	} else {
		c.logger.Info("here - else")
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

var null = json.RawMessage([]byte("null"))

func (c *codec) WriteResponse(r *rpc.Response, v any) error {
	c.logger.V(7).Info("writing response", "response", r, "object", v)
	if c.serverRequest.unMarshalledId == nil {
		c.logger.V(7).Info("dont respond on notifications")
		return nil
	}
	c.mutex.Lock()
	b, ok := c.pending[r.Seq]
	if !ok {
		c.mutex.Unlock()
		c.logger.Info("invalid sequence number in response", "number", r.Seq)
		return nil
	}
	delete(c.pending, r.Seq)
	c.mutex.Unlock()

	if b == nil {
		// Invalid request so no id.  Use JSON null.
		b = &null
	}
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
		n, err := c.connection.Write(([]byte(fmt.Sprintf(headerString, len(outBytes)))))
		if err != nil {
			c.logger.Info("unable to write header", "err", err)
			return nil
		}
		c.logger.V(7).Info("finshed writing language server header", "wrote", n)
	}
	n, err := c.connection.Write(outBytes)
	c.logger.V(7).Info("finished write response", "err", err, "bytes", n, "outBytes", string(outBytes))
	return nil
}

func (c *codec) ReadResponseBody(v any) error {
	c.logger.V(7).Info("read response body", "response", v)
	if v == nil {
		return nil
	}
	err := json.Unmarshal(*c.clientResponse.Result, v)
	c.logger.V(7).Info("finished read response body", "err", err, "body", v)
	return err
}

func (c *codec) Close() error {
	c.logger.Info("Calling Close!!!")
	c.connection.Close()
	return nil
}
