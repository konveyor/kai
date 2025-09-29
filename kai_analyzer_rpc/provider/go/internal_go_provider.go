//go:build !windows

package golang

import (
	"bufio"
	"context"
	"net"

	"github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	extgeneric "github.com/konveyor/analyzer-lsp/external-providers/generic-external-provider/pkg/generic_external_provider"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	clientwrapper "github.com/konveyor/kai-analyzer/pkg/rpc/client"
)

type InternalProviderClient struct {
	provider.BaseClient
	provider.ServiceClient
}

// NewInternalProviderClient creates a Go provider that connects to existing gopls via pipe
func NewInternalProviderClient(ctx context.Context, log logr.Logger, contextLines int, location, pipeFile string) (provider.InternalProviderClient, error) {
	p := extgeneric.NewGenericProvider("generic", log)

	providerConfig := map[string]interface{}{
		"lspServerName": "generic",
		"lspServerPath": "gopls",
	}

	conn, err := net.Dial("unix", pipeFile)
	if err != nil {
		return &InternalProviderClient{}, err
	}

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)
	c := codec.NewCodec(ctx, reader, writer, log.WithName("go-provider"), "", rpc2.NewState())
	client := rpc2.NewClientWithCodec(c)

	svcClient, _, err := p.Init(ctx, log, provider.InitConfig{
		Location:               location,
		Proxy:                  &provider.Proxy{},
		ProviderSpecificConfig: providerConfig,
		AnalysisMode:           "source-only",
		RPC: &clientwrapper.Client{
			Client: client,
		},
	})
	if err != nil {
		return &InternalProviderClient{}, err
	}

	return &InternalProviderClient{
		BaseClient:    p,
		ServiceClient: svcClient,
	}, nil
}

// NewInternalProviderClientForRPCClient creates a Go provider using existing RPC client
func NewInternalProviderClientForRPCClient(ctx context.Context, log logr.Logger, contextLines int, location string, client *rpc2.Client) (provider.InternalProviderClient, error) {
	p := extgeneric.NewGenericProvider("generic", log)

	providerConfig := map[string]interface{}{
		"lspServerName": "generic",
		"lspServerPath": "gopls", // Dummy path since we're using RPC connection
	}

	svcClient, _, err := p.Init(ctx, log, provider.InitConfig{
		Location:               location,
		Proxy:                  &provider.Proxy{},
		ProviderSpecificConfig: providerConfig,
		AnalysisMode:           "source-only",
		RPC: &clientwrapper.Client{
			Client: client,
		},
	})
	if err != nil {
		return &InternalProviderClient{}, err
	}

	return &InternalProviderClient{
		BaseClient:    p,
		ServiceClient: svcClient,
	}, nil
}

func (i *InternalProviderClient) ProviderInit(ctx context.Context, configs []provider.InitConfig) ([]provider.InitConfig, error) {
	return configs, nil
}
