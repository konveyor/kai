//go:build !windows

package rpc

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"net"
	"path/filepath"
	"sync/atomic"

	rpc "github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
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
	providerConfigFile      string
	progressReporter        progress.ProgressReporter
}

// NewServer creates a new RPC server instance for analyzer communication.
//
// The server manages the lifecycle of the analyzer service and handles
// RPC connections over Unix domain sockets.
//
// Parameters:
//   - ctx: Context for server lifecycle management
//   - s: Underlying RPC server implementation
//   - log: Logger for diagnostic output
//   - notificationServiceName: Name of the notification service to register
//   - rules: Comma-separated list of rule file paths
//   - providerConfigFile: Path to the provider configuration file
//   - progressReporter: Reporter for emitting analysis progress events
//
// The progressReporter is passed to the analyzer service and used to emit
// real-time progress updates during analysis operations.
func NewServer(ctx context.Context, s *rpc.Server, log logr.Logger, notificationServiceName string, rules string, providerConfigFile string, progressReporter progress.ProgressReporter) *Server {
	state := rpc.NewState()
	state.Set("seq", &atomic.Uint64{})
	return &Server{ctx: ctx,
		Server:                  s,
		log:                     log,
		state:                   state,
		notificationServiceName: notificationServiceName,
		rules:                   rules,
		providerConfigFile:      providerConfigFile,
		progressReporter:        progressReporter}
}

func (s *Server) Accept(pipePath string) {
	pipePath, err := filepath.Abs(pipePath)
	if err != nil {
		panic(err)
	}
	pipePath = filepath.Clean(pipePath)
	s.log.Info("dialing connection connections", "pipe", pipePath)
	lc := net.ListenConfig{}
	l, err := lc.Listen(s.ctx, "unix", pipePath)
	if err != nil {
		s.log.Error(err, "can not listen")
		panic(err)
	}
	// Register pipe analysis handler
	analyzerService, err := service.NewPipeAnalyzer(s.ctx, 10000, 10, 10, s.rules, s.providerConfigFile, s.log.WithName("analyzer-service"), s.progressReporter)
	if err != nil {
		s.log.Error(err, "unable to create analyzer service")
		panic(err)
	}
	s.Server.Handle("analysis_engine.Analyze", analyzerService.Analyze)
	// s.Server.Handle("analysis_engine.Stop", analyzerService.Stop)
	s.Server.Handle("analysis_engine.NotifyFileChanges", analyzerService.NotifyFileChanges)
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
