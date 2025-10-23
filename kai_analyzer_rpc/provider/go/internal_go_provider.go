//go:build !windows

package golang

import (
	"bufio"
	"context"
	"net"

	extgeneric "github.com/konveyor/analyzer-lsp/external-providers/generic-external-provider/pkg/generic_external_provider"

	"github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	clientwrapper "github.com/konveyor/kai-analyzer/pkg/rpc/client"
)

type InternalProviderClient struct {
	provider.BaseClient
	provider.ServiceClient
}

// NewInternalProviderClient creates a Go provider that connects to existing gopls via pipe
func NewInternalProviderClientForPipe(ctx context.Context, log logr.Logger, contextLines int, location, pipeFile, dependencyProviderPath string) (provider.InternalProviderClient, error) {
	log.Info("Initializing Go provider for pipe", "location", location, "pipeFile", pipeFile, "dependencyProviderPath", dependencyProviderPath)
	p := extgeneric.NewGenericProvider("generic", log)

	providerConfig := map[string]interface{}{
		"lspServerName":          "generic",
		"dependencyProviderPath": dependencyProviderPath,
	}
	log.Info("Go provider config for pipe", "config", providerConfig)

	conn, err := net.Dial("unix", pipeFile)
	if err != nil {
		return &InternalProviderClient{}, err
	}

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)
	c := codec.NewCodec(ctx, reader, writer, log.WithName("go-provider"), "", rpc2.NewState())
	client := rpc2.NewClientWithCodec(c)

	log.Info("About to call provider.Init for pipe", "config", providerConfig)
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
		log.Error(err, "provider.Init failed for pipe")
		return &InternalProviderClient{}, err
	} else {
		log.Info("provider.Init succeeded for pipe", "svcClient", svcClient)
	}

	return &InternalProviderClient{
		BaseClient:    p,
		ServiceClient: svcClient,
	}, nil
}

// NewInternalProviderClientForRPCClient creates a Go provider that uses an existing RPC client
func NewInternalProviderClientForRPCClient(ctx context.Context, log logr.Logger, contextLines int, location string, client *rpc2.Client, dependencyProviderPath string) (provider.InternalProviderClient, error) {
	p := extgeneric.NewGenericProvider("generic", log)

	providerConfig := map[string]interface{}{
		"lspServerName":          "generic",
		"dependencyProviderPath": dependencyProviderPath,
	}

	log.Info("About to call provider.Init", "config", providerConfig)
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
		log.Error(err, "provider.Init failed")
	} else {
		log.Info("provider.Init succeeded", "svcClient", svcClient)
	}
	if err != nil {
		return &InternalProviderClient{}, err
	}

	return &InternalProviderClient{
		BaseClient:    p,
		ServiceClient: svcClient,
	}, nil
}

// NewInternalProviderClient creates a Go provider that starts gopls directly using LSP path
func NewInternalProviderClient(ctx context.Context, log logr.Logger, contextLines int, location, lspServerPath, dependencyProviderPath string) (provider.InternalProviderClient, error) {
	log.Info("Initializing Go provider for direct LSP", "location", location, "lspServerPath", lspServerPath, "dependencyProviderPath", dependencyProviderPath)
	p := extgeneric.NewGenericProvider("generic", log)

	providerConfig := map[string]interface{}{
		"lspServerName":          "generic",
		"lspServerPath":          lspServerPath,
		"dependencyProviderPath": dependencyProviderPath,
	}
	log.Info("Go provider config for direct LSP", "config", providerConfig)

	svcClient, _, err := p.Init(ctx, log, provider.InitConfig{
		Location:               location,
		Proxy:                  &provider.Proxy{},
		ProviderSpecificConfig: providerConfig,
		AnalysisMode:           "source-only",
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
