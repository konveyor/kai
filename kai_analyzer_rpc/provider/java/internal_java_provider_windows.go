//go:build windows

package java

import (
	"bufio"
	"bytes"
	"context"

	"github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	extjava "github.com/konveyor/analyzer-lsp/external-providers/java-external-provider/pkg/java_external_provider"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	clientwrapper "github.com/konveyor/kai-analyzer/pkg/rpc/client"
)

type InternalProviderClient struct {
	provider.BaseClient
	provider.ServiceClient
}

func NewInternalProviderClient(ctx context.Context, log logr.Logger, contextLines int, location, lspServerPath, bundles, depOpenSourceLabelsFile string) (provider.InternalProviderClient, error) {
	// Create JavaProvider From external provider
	p := extjava.NewJavaProvider(log, "java", contextLines, provider.Config{
		Name: "java",
	})
	log.Info("logger", "v", p)
	providerConfig := map[string]interface{}{
		"lspServerName": "java",
		"bundles":       bundles,
		"lspServerPath": lspServerPath,
	}
	if depOpenSourceLabelsFile != "" {
		providerConfig["depOpenSourceLabelsFile"] = depOpenSourceLabelsFile
	}

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

func NewInternalProviderClientForPipe(ctx context.Context, log logr.Logger, contextLines int, location, pipeFile string) (provider.InternalProviderClient, error) {
	p := extjava.NewJavaProvider(log, "java", contextLines, provider.Config{
		Name: "java",
	})
	log.Info("logger", "v", p)
	providerConfig := map[string]interface{}{
		"lspServerName": "java",
	}

	reader := bufio.NewReader(bytes.NewBuffer([]byte{}))
	writer := bufio.NewWriter(bytes.NewBuffer([]byte{}))
	c := codec.NewCodec(ctx, reader, writer, log.WithName("provider"), "", rpc2.NewState())
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

func NewInternalProviderClientForRPCClient(ctx context.Context, log logr.Logger, contextLines int, location string, client *rpc2.Client) (provider.InternalProviderClient, error) {
	p := extjava.NewJavaProvider(log, "java", contextLines, provider.Config{
		Name: "java",
	})
	log.Info("logger", "v", p)
	providerConfig := map[string]interface{}{
		"lspServerName": "java",
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
