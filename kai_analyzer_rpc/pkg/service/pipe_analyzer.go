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
	"github.com/konveyor/analyzer-lsp/progress"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"
)

// NewPipeAnalyzer creates a new analyzer instance for pipe-based communication.
//
// This function initializes the analyzer with the specified configuration and emits
// progress events throughout the initialization process.
//
// Parameters:
//   - ctx: Context for cancellation and deadline control
//   - limitIncidents: Maximum number of incidents to report per rule
//   - limitCodeSnips: Maximum number of code snippets to include
//   - contextLines: Number of context lines to include around incidents
//   - rules: Comma-separated list of rule file paths
//   - providerConfigFile: Path to the provider configuration file
//   - l: Logger for diagnostic output
//   - progressReporter: Reporter for emitting progress events during analysis
//
// Progress events emitted:
//   - StageInit: When initialization begins
//   - StageProviderInit: During provider initialization (per provider)
//   - StageRuleParsing: After rules are loaded (includes total count)
//
// Returns an Analyzer instance or an error if initialization fails.
func NewPipeAnalyzer(ctx context.Context, limitIncidents, limitCodeSnips, contextLines int, rules, providerConfigFile string, l logr.Logger, progressReporter progress.ProgressReporter) (Analyzer, error) {
	// Emit init event
	progressReporter.Report(progress.ProgressEvent{
		Stage: progress.StageInit,
	})

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
			return nil, fmt.Errorf("you can only use an existing provider serving at a particular location")
		}
		for _, initConfig := range config.InitConfig {
			if initConfig.PipeName == "" {
				return nil, fmt.Errorf("the providers should only be using a pipe to communicate to the LSP")
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

	discoveryRulesets, violationRulesets, neededProviders, providerConditions, err := parseRules(parser, rules, l)
	if err != nil {
		return nil, fmt.Errorf("unable to parse rules: %w", err)
	}

	// Report rule parsing complete
	totalRules := 0
	for _, rs := range discoveryRulesets {
		totalRules += len(rs.Rules)
	}
	for _, rs := range violationRulesets {
		totalRules += len(rs.Rules)
	}
	progressReporter.Report(progress.ProgressEvent{
		Stage: progress.StageRuleParsing,
		Total: totalRules,
	})

	builtinConfigs := []provider.InitConfig{}
	for k, neededProvider := range neededProviders {
		switch k {
		case "builtin":
			continue
		default:
			l.Info("initing provider", "provider", k)
			progressReporter.Report(progress.ProgressEvent{
				Stage:   progress.StageProviderInit,
				Message: fmt.Sprintf("Initializing %s provider", k),
			})
			additionalBuiltinConfigs, err := neededProvider.ProviderInit(ctx, nil)
			if err != nil {
				return nil, err
			}
			progressReporter.Report(progress.ProgressEvent{
				Stage:   progress.StageProviderInit,
				Message: fmt.Sprintf("Provider %s ready", k),
			})
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
		if err != nil {
			return nil, err
		}
		providers["builtin"] = builtinClient
		_, err = builtinClient.ProviderInit(ctx, nil)
		if err != nil {
			return nil, err
		}
	}

	// Call Prepare() on all providers with the provider conditions
	for k, v := range providerConditions {
		if _, ok := neededProviders[k]; ok {
			if err := neededProviders[k].Prepare(ctx, v); err != nil {
				return nil, err
			}
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
		progressReporter:    progressReporter,
		//updateConditionProvider: updateProviderConditionToUseNewRPClientParseRules,
	}, nil

}

func parseRules(parser parser.RuleParser, rules string, l logr.Logger) ([]engine.RuleSet, []engine.RuleSet, map[string]provider.InternalProviderClient, map[string][]provider.ConditionsByCap, error) {
	discoveryRulesets := []engine.RuleSet{}
	violationRulesets := []engine.RuleSet{}
	neededProviders := map[string]provider.InternalProviderClient{}
	providerConditions := map[string][]provider.ConditionsByCap{}
	for _, f := range strings.Split(rules, ",") {
		internRuleSets, newNeededProviders, provConditions, err := parser.LoadRules(strings.TrimSpace(f))
		if err != nil {
			l.Error(err, "unable to parse all the rules for ruleset", "file", f)
			return nil, nil, nil, nil, err
		}
		for k, v := range newNeededProviders {
			neededProviders[k] = v
		}
		for k, v := range provConditions {
			if _, ok := providerConditions[k]; !ok {
				providerConditions[k] = []provider.ConditionsByCap{}
			}
			providerConditions[k] = append(providerConditions[k], v...)
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
	return discoveryRulesets, violationRulesets, neededProviders, providerConditions, nil
}
