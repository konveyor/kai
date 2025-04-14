// go: build linux || darwin || freebsd || openbsd || netbsd || solaris || dragonfly || plan9
package service

import (
	"context"
	"path/filepath"
	"sync"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"
)

func NewPipeAnalyzer(limitIncidents, limitCodeSnips, contextLines int, pipePath, rules, location string, l logr.Logger) (Analyzer, error) {
	prefix, err := filepath.Abs(location)
	if err != nil {
		return nil, err
	}
	ctx, cancelFunc := context.WithCancel(context.Background())
	eng := engine.CreateRuleEngine(ctx,
		10,
		l,
		engine.WithIncidentLimit(limitIncidents),
		engine.WithCodeSnipLimit(limitCodeSnips),
		engine.WithContextLines(contextLines),
		//engine.WithIncidentSelector(incidentSelector),
		engine.WithLocationPrefixes([]string{prefix}),
	)

	// this function already init's the java provider
	///jProvider, err := java.NewInternalProviderClient(ctx, l, contextLines, location, lspServerPath, bundles, depOpenSourceLabelsFile)
	//if err != nil {
	//cancelFunc()
	//return nil, err
	//}

	bProvider, err := lib.GetProviderClient(provider.Config{Name: "builtin"}, l)
	if err != nil {
		cancelFunc()
		return nil, err
	}
	_, err = bProvider.ProviderInit(context.Background(), []provider.InitConfig{{Location: location}})
	if err != nil {
		cancelFunc()
		return nil, err
	}

	providers := map[string]provider.InternalProviderClient{
		// "java":    jProvider,
		"builtin": bProvider,
	}

	// parser := parser.RuleParser{
	// 	ProviderNameToClient: providers,
	// 	Log:                  l.WithName("parser"),
	// }

	discoveryRulesets := []engine.RuleSet{}
	violationRulesets := []engine.RuleSet{}
	// for _, f := range strings.Split(rules, ",") {
	// 	internRuleSets, _, err := parser.LoadRules(strings.TrimSpace(f))
	// 	if err != nil {
	// 		l.Error(err, "unable to parse all the rules for ruleset", "file", f)
	// 		cancelFunc()
	// 		return nil, err
	// 	}

	// 	for _, interimRuleSet := range internRuleSets {
	// 		runCacheResetRuleset := engine.RuleSet{
	// 			Name:        interimRuleSet.Name,
	// 			Description: interimRuleSet.Description,
	// 			Labels:      interimRuleSet.Labels,
	// 			Tags:        interimRuleSet.Tags,
	// 			Rules:       []engine.Rule{},
	// 		}
	// 		allOtherRuleSet := engine.RuleSet{
	// 			Name:        interimRuleSet.Name,
	// 			Description: interimRuleSet.Description,
	// 			Labels:      interimRuleSet.Labels,
	// 			Tags:        interimRuleSet.Tags,
	// 			Rules:       []engine.Rule{},
	// 		}
	// 		for _, interimRule := range interimRuleSet.Rules {
	// 			hasDiscovery, hasAlways := labelsContainDiscoveryOrAlways(append(interimRule.Labels, interimRuleSet.Labels...))
	// 			if len(interimRule.Labels) == 2 && hasDiscovery && hasAlways {
	// 				runCacheResetRuleset.Rules = append(runCacheResetRuleset.Rules, interimRule)
	// 			} else if interimRule.Perform.Tag != nil && !(interimRule.Perform.Message.Text != nil && interimRule.Effort != nil && *interimRule.Effort != 0) {
	// 				// We want to pull out tagging rules and insight only rules
	// 				// These don't generate violations, and we should treat them
	// 				// like discovery rules
	// 				runCacheResetRuleset.Rules = append(runCacheResetRuleset.Rules, interimRule)
	// 			} else {
	// 				allOtherRuleSet.Rules = append(allOtherRuleSet.Rules, interimRule)
	// 			}
	// 		}

	// 		if len(allOtherRuleSet.Rules) > 0 {
	// 			violationRulesets = append(violationRulesets, allOtherRuleSet)
	// 		}
	// 		if len(runCacheResetRuleset.Rules) > 0 {
	// 			discoveryRulesets = append(discoveryRulesets, runCacheResetRuleset)
	// 		}
	// 	}
	// }

	l.Info("using rulesets", "discoverRulesets", len(discoveryRulesets), "violationRulesets", len(violationRulesets))
	// Generate discoveryRulesetCache here??

	return &analyzer{
		Logger:              l,
		engine:              eng,
		engineCtx:           ctx,
		cancelFunc:          cancelFunc,
		initedProviders:     providers,
		discoveryRulesets:   discoveryRulesets,
		violationRulesets:   violationRulesets,
		discoveryCache:      []konveyor.RuleSet{},
		discoveryCacheMutex: sync.Mutex{},
		cache:               map[string][]cacheValue{},
		cacheMutex:          sync.RWMutex{},
	}, nil

}
