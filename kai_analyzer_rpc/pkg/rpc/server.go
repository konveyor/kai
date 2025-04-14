package rpc

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"net"
	"sync/atomic"

	rpc "github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	"github.com/konveyor/kai-analyzer/pkg/service"
)

type Server struct {
	*rpc.Server
	ctx                     context.Context
	log                     logr.Logger
	state                   *rpc.State
	notificationServiceName string
	connections             []net.Conn
	rules                   string
	sourceDirectory         string
}

func NewServer(ctx context.Context, s *rpc.Server, log logr.Logger, notificationServiceName string, rules string, sourceDirectory string) *Server {
	state := rpc.NewState()
	state.Set("seq", &atomic.Uint64{})
	return &Server{ctx: ctx,
		Server:                  s,
		log:                     log,
		state:                   state,
		notificationServiceName: notificationServiceName,
		rules:                   rules,
		sourceDirectory:         sourceDirectory}
}

func (s *Server) Accept(pipePath string) {
	s.log.Info("dialing connection connections")
	lc := net.ListenConfig{}
	l, err := lc.Listen(s.ctx, "unix", pipePath)
	if err != nil {
		s.log.Error(err, "can not listen")
	}
	// Register pipe analysis handler
	analyzerService, err := service.NewPipeAnalyzer(s.ctx, 10000, 10, 10, pipePath, s.rules, s.sourceDirectory, s.log.WithName("analyzer-service"))
	if err != nil {
		s.log.Error(err, "unable to create analyzer service")
		return
	}
	s.Server.Handle("analysis_engine.Analyze", analyzerService.Analyze)
	for {
		conn, err := l.Accept()
		if err != nil {
			if !errors.Is(err, net.ErrClosed) {
				s.log.Info("rpc.Serve: accept:", err.Error())
			}
			return
		}
		s.connections = append(s.connections, conn)
		s.log.Info("got connection", "conn", fmt.Sprintf("%v", conn))
		go s.run(conn)
	}
}
func (s *Server) run(conn net.Conn) {
	s.log.Info("connection", "localAddr", conn.LocalAddr(), "remoteAddr", conn.RemoteAddr())
	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)
	c := codec.NewCodec(s.ctx, reader, writer, s.log.WithName("conn"), s.notificationServiceName, s.state)
	s.log.Info("server codec", "codec", fmt.Sprintf("%+v", c))
	s.Server.ServeCodecWithState(c, s.state)
	s.log.Info("here not in run")
}

func (s *Server) ServeCodecWithState(codec codec.Codec, state *rpc.State) {

}
