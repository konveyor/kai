package codec

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/rpc"
	"net/rpc/jsonrpc"
	"sync"

	"github.com/go-logr/logr"
)

// Connection wraps a pair of unidirectional streams as an io.ReadWriteCloser.
type Connection struct {
	Input  io.ReadCloser
	Output io.WriteCloser
}

// Read implements io.ReadWriteCloser.
func (c *Connection) Read(p []byte) (n int, err error) {
	return c.Input.Read(p)
}

// Write implements io.ReadWriteCloser.
func (c *Connection) Write(p []byte) (n int, err error) {
	return c.Output.Write(p)
}

// Close closes c's underlying ReadCloser and WriteCloser.
func (c *Connection) Close() error {
	rerr := c.Input.Close()
	werr := c.Output.Close()
	if rerr != nil {
		return rerr
	}
	return werr
}

type Codec interface {
	rpc.ClientCodec
	rpc.ServerCodec
}

type codec struct {
	rpc.ClientCodec
	rpc.ServerCodec
	logger logr.Logger
}

func (c *codec) WriteRequest(r *rpc.Request, v any) error {
	c.logger.V(7).Info("write request", "request", r, "value", v)
	err := c.ClientCodec.WriteRequest(r, v)
	c.logger.V(7).Info("finished request header", "err", err, "request", r)
	return err
}

func (c *codec) ReadRequestHeader(r *rpc.Request) error {
	c.logger.V(7).Info("read request header", "request", r)
	err := c.ServerCodec.ReadRequestHeader(r)
	c.logger.V(7).Info("finished request header", "err", err, "request", r)
	return err
}

func (c *codec) ReadRequestBody(r any) error {
	c.logger.V(7).Info("read request body", "request", r)
	err := c.ServerCodec.ReadRequestBody(r)
	c.logger.V(7).Info("finished request body", "err", err, "request", r)
	return err
}

func (c *codec) WriteResponse(r *rpc.Response, v any) error {
	c.logger.V(7).Info("writing response", "response", r, "object", v)
	err := c.ServerCodec.WriteResponse(r, v)
	c.logger.V(7).Info("finished write response", "err", err)
	return err
}

func (c *codec) Close() error {
	err := c.ClientCodec.Close()
	if err != nil {
		return err
	}
	err = c.ServerCodec.Close()
	if err != nil {
		return err
	}
	return nil
}

func NewCodec(connection Connection, logger logr.Logger) Codec {
	return &codec{
		ClientCodec: jsonrpc.NewClientCodec(&connection), ServerCodec: NewServerCodec(&connection, logger),
		logger: logger.WithName("json codec"),
	}
}

type serverCodec struct {
	dec *json.Decoder // for reading JSON values
	enc *json.Encoder // for writing JSON values
	c   io.Closer

	// temporary work space
	req serverRequest

	// JSON-RPC clients can use arbitrary json values as request IDs.
	// Package rpc expects uint64 request IDs.
	// We assign uint64 sequence numbers to incoming requests
	// but save the original request ID in the pending map.
	// When rpc responds, we use the sequence number in
	// the response to find the original request ID.
	mutex   sync.Mutex // protects seq, pending
	seq     uint64
	pending map[uint64]*json.RawMessage

	logger logr.Logger
}

func NewServerCodec(conn io.ReadWriteCloser, log logr.Logger) rpc.ServerCodec {
	return &serverCodec{
		dec:     json.NewDecoder(conn),
		enc:     json.NewEncoder(conn),
		c:       conn,
		pending: make(map[uint64]*json.RawMessage),
		logger:  log,
	}
}

type serverRequest struct {
	Method string           `json:"method"`
	Params *json.RawMessage `json:"params"`
	Id     *json.RawMessage `json:"id"`
}

func (r *serverRequest) reset() {
	r.Method = ""
	r.Params = nil
	r.Id = nil
}

type serverResponse struct {
	Id     *json.RawMessage `json:"id"`
	Result any              `json:"result"`
	Error  any              `json:"error"`
}

func (c *serverCodec) ReadRequestHeader(r *rpc.Request) error {
	c.req.reset()
	if err := c.dec.Decode(&c.req); err != nil {
		return err
	}
	r.ServiceMethod = c.req.Method

	// JSON request id can be any JSON value;
	// RPC package expects uint64.  Translate to
	// internal uint64 and save JSON on the side.
	c.mutex.Lock()
	c.seq++
	c.pending[c.seq] = c.req.Id
	c.req.Id = nil
	r.Seq = c.seq
	c.mutex.Unlock()

	return nil
}

func (c *serverCodec) ReadRequestBody(x any) error {
	if x == nil {
		return nil
	}
	if c.req.Params == nil {
		return fmt.Errorf("invalid params")
	}
	// JSON params is array value.
	// RPC params is struct.
	// Unmarshal into array containing struct for now.
	// Should think about making RPC more general.
	var params [1]any
	params[0] = x
	return json.Unmarshal(*c.req.Params, &params)
}

var null = json.RawMessage([]byte("null"))

func (c *serverCodec) WriteResponse(r *rpc.Response, x any) error {
	c.logger.V(7).Info("writing response", "id", r.Seq, "pending", c.pending)
	c.mutex.Lock()
	b, ok := c.pending[r.Seq]
	if !ok {
		c.mutex.Unlock()
		return errors.New("invalid sequence number in response")
	}
	delete(c.pending, r.Seq)
	c.mutex.Unlock()

	if b == nil {
		// Invalid request so no id. Use JSON null.
		b = &null
	}
	resp := serverResponse{Id: b}
	if r.Error == "" {
		resp.Result = x
	} else {
		resp.Error = r.Error
	}
	return c.enc.Encode(resp)
}

func (c *serverCodec) Close() error {
	return c.c.Close()
}

// ServeConn runs the JSON-RPC server on a single connection.
// ServeConn blocks, serving the connection until the client hangs up.
// The caller typically invokes ServeConn in a go statement.
func ServeConn(conn io.ReadWriteCloser) {
	rpc.ServeCodec(NewServerCodec(conn, logr.FromContextOrDiscard(context.Background())))
}
