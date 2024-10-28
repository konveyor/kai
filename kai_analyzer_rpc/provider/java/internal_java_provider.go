package java

import (
	"context"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/provider"
	extjava "github.com/shawn-hurley/java-external-provider/pkg/java_external_provider"
)

type InternalProviderClient struct {
	provider.BaseClient
	provider.ServiceClient
}

func NewInternalProviderClient(ctx context.Context, log logr.Logger, contextLines int, location, lspServerPath, bundles, depOpenSourceLabelsFile string) (provider.InternalProviderClient, error) {
	// Create JavaProvider From external provider
	p := extjava.NewJavaProvider(log, "java", contextLines)
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

func (i *InternalProviderClient) ProviderInit(ctx context.Context, configs []provider.InitConfig) ([]provider.InitConfig, error) {
	return configs, nil
}
