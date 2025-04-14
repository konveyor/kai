package rpc

import (
	"errors"
	"fmt"
	"net"
	"sync"

	rpc "github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
)

type Server struct {
	*rpc.Server
	log                     logr.Logger
	state                   *rpc.State
	wg                      *sync.WaitGroup
	notificationServiceName string
}

func NewServer(s *rpc.Server, log logr.Logger, wg *sync.WaitGroup, notificationServiceName string) *Server {
	state := rpc.NewState()
	return &Server{Server: s, log: log, state: state, wg: wg, notificationServiceName: notificationServiceName}
}

func (s *Server) Accept(pipePath string) {
	s.log.Info("dialing connection connections")
	conn, err := net.Dial("unix", pipePath)
	s.log.Info("connection", "localAddr", conn.LocalAddr(), "remoteAddr", conn.RemoteAddr())
	if err != nil {
		if !errors.Is(err, net.ErrClosed) {
			s.log.Info("rpc.Serve: accept:", err.Error())
		}
		return
	}
	s.log.Info("state", "state", fmt.Sprintf("%#v", s.state))
	s.log.Info("server", "server", fmt.Sprintf("%#v", s.Server))
	s.wg.Done()
	s.Server.ServeCodecWithState(codec.NewCodec(conn, s.log, s.notificationServiceName), s.state)

}
