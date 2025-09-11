// go: build linux || darwin || freebsd || openbsd || netbsd || solaris || dragonfly || plan9
package service

import (
	"context"
	"errors"
	"path/filepath"
	"strings"
	"sync"

	"github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/parser"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"
	golang "github.com/konveyor/kai-analyzer/provider/go"
	"github.com/konveyor/kai-analyzer/provider/java"
)

func NewPipeAnalyzer(ctx context.Context, limitIncidents, limitCodeSnips, contextLines int, pipePath, rules, location, language, lspServerPath, bundles, depOpenSourceLabelsFile, goplsPipe string, l logr.Logger) (Analyzer, error) {
	prefix, err := filepath.Abs(location)
	if err != nil {
		return nil, err
	}
	ctx, cancelFunc := context.WithCancel(ctx)
	eng := engine.CreateRuleEngine(ctx,
		10,
		l,
		engine.WithIncidentLimit(limitIncidents),
		engine.WithCodeSnipLimit(limitCodeSnips),
		engine.WithContextLines(contextLines),
		//engine.WithIncidentSelector(incidentSelector),
		engine.WithLocationPrefixes([]string{prefix}),
	)

	// Initialize builtin provider (always needed)
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
		"builtin": bProvider,
	}

	// Initialize language-specific provider based on language parameter
	l.Info("About to initialize provider", "language", language)
	switch language {
	case "java":
		l.Info("Initializing Java provider for pipe", "pipePath", pipePath, "lspServerPath", lspServerPath, "bundles", bundles)
		jProvider, err := java.NewInternalProviderClientForPipe(ctx, l, contextLines, location, pipePath)
		if err != nil {
			cancelFunc()
			return nil, err
		}
		providers["java"] = jProvider
		l.Info("Java provider initialized successfully")

	case "go":
		l.Info("Initializing Go provider for pipe", "goplsPipe", goplsPipe)
		goProvider, err := golang.NewInternalProviderClient(ctx, l, contextLines, location, goplsPipe)
		if err != nil {
			cancelFunc()
			return nil, err
		}
		providers["go"] = goProvider
		l.Info("Go provider initialized successfully")

	default:
		cancelFunc()
		return nil, errors.New("unsupported language: " + language + ". Supported languages: java, go")
	}

	parser := parser.RuleParser{
		ProviderNameToClient: providers,
		Log:                  l.WithName("parser"),
	}

	discoveryRulesets, violationRulesets, err := parseRules(parser, rules, l, cancelFunc)
	if err != nil {
		return nil, err
	}

	l.Info("using rulesets", "discoverRulesets", len(discoveryRulesets), "violationRulesets", len(violationRulesets))
	// Generate discoveryRulesetCache here??

	return &analyzer{
		Logger:                  l,
		engine:                  eng,
		engineCtx:               ctx,
		cancelFunc:              cancelFunc,
		initedProviders:         providers,
		discoveryRulesets:       discoveryRulesets,
		violationRulesets:       violationRulesets,
		discoveryCache:          []konveyor.RuleSet{},
		discoveryCacheMutex:     sync.Mutex{},
		cache:                   map[string][]cacheValue{},
		cacheMutex:              sync.RWMutex{},
		location:                location,
		contextLines:            contextLines,
		rules:                   rules,
		updateConditionProvider: updateProviderConditionToUseNewRPClientParseRules,
	}, nil

}

func parseRules(parser parser.RuleParser, rules string, l logr.Logger, cancelFunc func()) ([]engine.RuleSet, []engine.RuleSet, error) {
	discoveryRulesets := []engine.RuleSet{}
	violationRulesets := []engine.RuleSet{}
	for _, f := range strings.Split(rules, ",") {
		internRuleSets, _, err := parser.LoadRules(strings.TrimSpace(f))
		if err != nil {
			l.Error(err, "unable to parse all the rules for ruleset", "file", f)
			cancelFunc()
			return nil, nil, err
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
	return discoveryRulesets, violationRulesets, nil
}

func updateProviderConditionToUseNewRPClientParseRules(client *rpc2.Client,
	existingProviders map[string]provider.InternalProviderClient,
	discoveryRulesets, violationRulesets []engine.RuleSet,
	log logr.Logger,
	contextLines int,
	location, rules string) ([]engine.RuleSet, []engine.RuleSet, error) {

	jProvider, err := java.NewInternalProviderClientForRPCClient(context.TODO(), log, contextLines, location, client)
	if err != nil {
		return nil, nil, err
	}

	var bProvider provider.InternalProviderClient
	if val, ok := existingProviders["builtin"]; ok {
		bProvider = val
	} else {
		bProvider, err := lib.GetProviderClient(provider.Config{Name: "builtin"}, log)
		if err != nil {
			return nil, nil, err
		}
		_, err = bProvider.ProviderInit(context.Background(), []provider.InitConfig{{Location: location}})
		if err != nil {
			return nil, nil, err
		}
	}

	providers := map[string]provider.InternalProviderClient{
		"java":    jProvider,
		"builtin": bProvider,
	}

	parser := parser.RuleParser{
		ProviderNameToClient: providers,
		Log:                  log.WithName("parser"),
	}
	return parseRules(parser, rules, log, func() {})
}

// TODO: This code was not working but should work and should be the more correct way to do this rather then re-parsing rules.
// func updateProviderConditionToUseNewRPClient(client *rpc2.Client,
// 	discoveryRulesets, violationRulesets []engine.RuleSet,
// 	log logr.Logger,
// 	contextLines int,
// 	location, _ string) ([]engine.RuleSet, []engine.RuleSet, error) {
// 	//create new java provider

// 	c, err := java.NewInternalProviderClientForRPCClient(context.TODO(), log, contextLines, location, client)
// 	if err != nil {
// 		return nil, nil, err
// 	}
// 	client.Notify("started", nil)
// 	reply := map[string]interface{}{}
// 	client.Call("workspace/executeCommand", []map[string]interface{}{{"command": "io.konveyor.tackle.ruleEntry",
// 		"arguments": map[string]interface{}{
// 			"analysisMode": "source-only",
// 			"location":     "11",
// 			"project":      "java",
// 			"query":        "java.rmi*"},
// 		"id":      1,
// 		"jsonrpc": "2.0"}}, reply)

// 	for _, rs := range discoveryRulesets {
// 		for _, r := range rs.Rules {
// 			switch r.When.(type) {
// 			case engine.ConditionEntry:
// 				log.Info("dealing with simplest case", "before", fmt.Sprintf("%+v", r.When))
// 				v := r.When.(engine.ConditionEntry)
// 				if x, ok := v.ProviderSpecificConfig.(provider.ProviderCondition); ok {
// 					if strings.Contains(reflect.TypeOf(x.Client).String(), "java") {
// 						x.Client = c
// 						v.ProviderSpecificConfig = x
// 					}
// 					r.When = v
// 					log.Info("dealing with simplest case", "after", fmt.Sprintf("%+v", r.When))
// 				}
// 			case engine.AndCondition:
// 				v := r.When.(engine.AndCondition)
// 				conditions := handleConditionEntries(v.Conditions, c)
// 				v.Conditions = conditions
// 				r.When = v
// 			case engine.OrCondition:
// 				v := r.When.(engine.OrCondition)
// 				conditions := handleConditionEntries(v.Conditions, c)
// 				v.Conditions = conditions
// 				r.When = v
// 			default:
// 				panic(fmt.Errorf("invalid top level condition when type: %T -- %+v", r.When, r.When))
// 			}
// 		}
// 	}
// 	for _, rs := range violationRulesets {
// 		for _, r := range rs.Rules {
// 			switch r.When.(type) {
// 			case engine.ConditionEntry:
// 				v := r.When.(engine.ConditionEntry)
// 				if x, ok := v.ProviderSpecificConfig.(provider.ProviderCondition); ok {
// 					if strings.Contains(reflect.TypeOf(x.Client).String(), "java") {
// 						x.Client = c
// 						v.ProviderSpecificConfig = x
// 					}
// 				}
// 				r.When = v
// 			case engine.AndCondition:
// 				v := r.When.(engine.AndCondition)
// 				conditions := handleConditionEntries(v.Conditions, c)
// 				v.Conditions = conditions
// 				r.When = v
// 			case engine.OrCondition:
// 				v := r.When.(engine.OrCondition)
// 				conditions := handleConditionEntries(v.Conditions, c)
// 				v.Conditions = conditions
// 				r.When = v
// 			default:
// 				panic(fmt.Errorf("invalid top level condition when type: %T -- %+v", r.When, r.When))
// 			}

// 		}
// 	}
// 	return discoveryRulesets, violationRulesets, nil
// }

// func handleConditionEntries(entries []engine.ConditionEntry, c provider.InternalProviderClient) []engine.ConditionEntry {
// 	ret := []engine.ConditionEntry{}
// 	for _, ce := range entries {
// 		switch ce.ProviderSpecificConfig.(type) {
// 		case engine.ConditionEntry:
// 			v := ce.ProviderSpecificConfig.(engine.ConditionEntry)
// 			if x, ok := v.ProviderSpecificConfig.(provider.ProviderCondition); ok {
// 				x.Client = c
// 				v.ProviderSpecificConfig = x
// 			}
// 			ret = append(ret, ce)
// 		case engine.AndCondition:
// 			v := ce.ProviderSpecificConfig.(engine.AndCondition)
// 			conditions := handleConditionEntries(v.Conditions, c)
// 			v.Conditions = conditions
// 			ce.ProviderSpecificConfig = v
// 			ret = append(ret, ce)

// 		case engine.OrCondition:
// 			v := ce.ProviderSpecificConfig.(engine.OrCondition)
// 			conditions := handleConditionEntries(v.Conditions, c)
// 			v.Conditions = conditions
// 			ce.ProviderSpecificConfig = v
// 			ret = append(ret, ce)
// 		}
// 	}
// 	return ret
// }
