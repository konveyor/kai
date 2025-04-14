package codec

import (
	"io"

	"github.com/cenkalti/rpc2"
	"github.com/cenkalti/rpc2/jsonrpc"
	"github.com/go-logr/logr"
)

// Connection wraps a pair of unidirectional streams as an io.ReadWriteCloser.
type Connection struct {
	Input  io.ReadCloser
	Output io.WriteCloser
	Logger logr.Logger
}

// Read implements io.ReadWriteCloser.
func (c Connection) Read(p []byte) (n int, err error) {
	r, err := c.Input.Read(p)
	c.Logger.Info("read from connection", "bytes read", r, "error", err, "bytes", string(p))
	return r, err

}

// Write implements io.ReadWriteCloser.
func (c Connection) Write(p []byte) (n int, err error) {
	return c.Output.Write(p)
}

// Close closes c's underlying ReadCloser and WriteCloser.
func (c Connection) Close() error {
	rerr := c.Input.Close()
	werr := c.Output.Close()
	if rerr != nil {
		return rerr
	}
	return werr
}

type connectionCodec struct {
	rpc2.Codec
	log logr.Logger
}

func NewConnectionCodec(connection Connection, log logr.Logger) rpc2.Codec {
	c := jsonrpc.NewJSONCodec(connection)
	return connectionCodec{
		Codec: c,
		log:   log.WithName("connection-codec"),
	}
}
