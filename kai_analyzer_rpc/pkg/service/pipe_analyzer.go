// go: build linux || darwin || freebsd || openbsd || netbsd || solaris || dragonfly || plan9
package service

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"sync"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/parser"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"
)

func NewPipeAnalyzer(ctx context.Context, limitIncidents, limitCodeSnips, contextLines int, rules, providerConfigFile string, l logr.Logger) (Analyzer, error) {
	ctx, cancelFunc := context.WithCancel(ctx)
	defer cancelFunc()
	// Get the providers from the provider config.
	l.Info("getting provider config", "config", providerConfigFile)
	configs, err := provider.GetConfig(providerConfigFile)
	if err != nil {
		return nil, errors.Join(err, errors.New("unable to get provider config"))
	}

	l.Info("got provider config", "config", providerConfigFile, "configs", configs)
	providers := map[string]provider.InternalProviderClient{}
	defaultBuiltinConfigs := []provider.InitConfig{}
	locations := []string{}
	for _, config := range configs {
		if config.Address == "" || config.BinaryPath != "" {
			return nil, fmt.Errorf("You can only use an existing provider serving at a particular location")
		}
		for _, initConfig := range config.InitConfig {
			if initConfig.PipeName == "" {
				return nil, fmt.Errorf("The providers should only be using a pipe to communicate to the LSP")
			}
			locations = append(locations, initConfig.Location)
			defaultBuiltinConfigs = append(defaultBuiltinConfigs, provider.InitConfig{
				Location: initConfig.Location,
			})
		}
		providerClient, err := lib.GetProviderClient(config, l)
		if err != nil {
			return nil, err
		}
		providers[config.Name] = providerClient
	}
	if _, ok := providers["builtin"]; !ok {
		// Have to add the builtin provider here
		builtinClient, err := lib.GetProviderClient(provider.Config{
			Name:       "builtin",
			InitConfig: defaultBuiltinConfigs,
		}, l)
		if err != nil {
			return nil, err
		}
		providers["builtin"] = builtinClient
	}

	parser := parser.RuleParser{
		ProviderNameToClient: providers,
		Log:                  l.WithName("parser"),
	}

	discoveryRulesets, violationRulesets, neededProviders, err := parseRules(parser, rules, l, cancelFunc)
	if err != nil {
		return nil, err
	}
	builtinConfigs := []provider.InitConfig{}
	for k, neededProvider := range neededProviders {
		switch k {
		case "builtin":
			continue
		default:
			l.Info("initing provider", "provider", k)
			additionalBuiltinConfigs, err := neededProvider.ProviderInit(ctx, nil)
			if err != nil {
				return nil, err
			}
			builtinConfigs = append(builtinConfigs, additionalBuiltinConfigs...)
		}
	}
	if builtinClient, ok := neededProviders["builtin"]; ok {
		if _, err = builtinClient.ProviderInit(ctx, builtinConfigs); err != nil {
			return nil, err
		}
	} else {
		builtinClient, err := lib.GetProviderClient(provider.Config{
			Name:       "builtin",
			InitConfig: defaultBuiltinConfigs,
		}, l)
		providers["builtin"] = builtinClient
		_, err = builtinClient.ProviderInit(ctx, nil)
		if err != nil {
			return nil, err
		}
	}

	ctx, cancelFunc = context.WithCancel(context.Background())
	eng := engine.CreateRuleEngine(ctx,
		10,
		l,
		engine.WithIncidentLimit(limitIncidents),
		engine.WithCodeSnipLimit(limitCodeSnips),
		engine.WithContextLines(contextLines),
		engine.WithLocationPrefixes(locations),
	)

	l.Info("using rulesets", "discoverRulesets", len(discoveryRulesets), "violationRulesets", len(violationRulesets))
	// Generate discoveryRulesetCache here??

	return &analyzer{
		Logger:              l,
		engine:              eng,
		engineCtx:           ctx,
		cancelFunc:          cancelFunc,
		initedProviders:     neededProviders,
		discoveryRulesets:   discoveryRulesets,
		violationRulesets:   violationRulesets,
		discoveryCache:      []konveyor.RuleSet{},
		discoveryCacheMutex: sync.Mutex{},
		cache:               NewIncidentsCache(l),
		locations:           locations,
		contextLines:        contextLines,
		rules:               rules,
		//updateConditionProvider: updateProviderConditionToUseNewRPClientParseRules,
	}, nil

}

func parseRules(parser parser.RuleParser, rules string, l logr.Logger, cancelFunc func()) ([]engine.RuleSet, []engine.RuleSet, map[string]provider.InternalProviderClient, error) {
	discoveryRulesets := []engine.RuleSet{}
	violationRulesets := []engine.RuleSet{}
	neededProviders := map[string]provider.InternalProviderClient{}
	for _, f := range strings.Split(rules, ",") {
		internRuleSets, newNeededProviders, err := parser.LoadRules(strings.TrimSpace(f))
		if err != nil {
			l.Error(err, "unable to parse all the rules for ruleset", "file", f)
			cancelFunc()
			return nil, nil, nil, err
		}
		for k, v := range newNeededProviders {
			neededProviders[k] = v
		}

		for _, interimRuleSet := range internRuleSets {
			runCacheResetRuleset := engine.RuleSet{
				Name:        interimRuleSet.Name,
				Description: interimRuleSet.Description,
				Labels:      interimRuleSet.Labels,
				Tags:        interimRuleSet.Tags,
				Rules:       []engine.Rule{},
			}
			allOtherRuleSet := engine.RuleSet{
				Name:        interimRuleSet.Name,
				Description: interimRuleSet.Description,
				Labels:      interimRuleSet.Labels,
				Tags:        interimRuleSet.Tags,
				Rules:       []engine.Rule{},
			}
			for _, interimRule := range interimRuleSet.Rules {
				hasDiscovery, hasAlways := labelsContainDiscoveryOrAlways(append(interimRule.Labels, interimRuleSet.Labels...))
				if len(interimRule.Labels) == 2 && hasDiscovery && hasAlways {
					runCacheResetRuleset.Rules = append(runCacheResetRuleset.Rules, interimRule)
				} else if interimRule.Perform.Tag != nil && !(interimRule.Perform.Message.Text != nil && interimRule.Effort != nil && *interimRule.Effort != 0) {
					// We want to pull out tagging rules and insight only rules
					// These don't generate violations, and we should treat them
					// like discovery rules
					runCacheResetRuleset.Rules = append(runCacheResetRuleset.Rules, interimRule)
				} else {
					allOtherRuleSet.Rules = append(allOtherRuleSet.Rules, interimRule)
				}
			}

			if len(allOtherRuleSet.Rules) > 0 {
				violationRulesets = append(violationRulesets, allOtherRuleSet)
			}
			if len(runCacheResetRuleset.Rules) > 0 {
				discoveryRulesets = append(discoveryRulesets, runCacheResetRuleset)
			}
		}
	}
	return discoveryRulesets, violationRulesets, neededProviders, nil
}
