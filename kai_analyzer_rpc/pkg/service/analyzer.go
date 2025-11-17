package service

import (
	"context"
	"errors"
	"sort"
	"sync"

	rpc "github.com/cenkalti/rpc2"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/engine/labels"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/progress"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/kai-analyzer/pkg/scope"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
)

const (
	name                 = "konveyor.io/analysis-engine-rpc"
	DISCOVERY_LABEL      = "konveyor.io/target=discovery"
	ALWAYS_INCLUDE_LABEL = "konveyor.io/include=always"
)

var (
	tracer = otel.Tracer(name)
)

type Analyzer interface {
	Analyze(client *rpc.Client, args Args, response *Response) error
	NotifyFileChanges(client *rpc.Client, changes NotifyFileChangesArgs, response *NotifyFileChangesResponse) error
	Stop()
}

type NotifyFileChangesArgs struct {
	Changes []provider.FileChange
}

type NotifyFileChangesResponse struct {
	err error
}

type analyzer struct {
	Logger logr.Logger

	engine     engine.RuleEngine
	engineCtx  context.Context
	cancelFunc context.CancelFunc

	initedProviders   map[string]provider.InternalProviderClient
	discoveryRulesets []engine.RuleSet
	violationRulesets []engine.RuleSet

	discoveryCacheMutex sync.Mutex
	discoveryCache      []konveyor.RuleSet
	cache               IncidentsCache

	contextLines int
	locations    []string
	rules        string

	progressReporter progress.ProgressReporter

	updateConditionProvider func(*rpc.Client, map[string]provider.InternalProviderClient, []engine.RuleSet, []engine.RuleSet, logr.Logger, int, string, string) ([]engine.RuleSet, []engine.RuleSet, error)
}

/*
func NewAnalyzer(limitIncidents, limitCodeSnips, contextLines int, location, incidentSelector, lspServerPath, bundles, depOpenSourceLabelsFile, rules string, log logr.Logger) (Analyzer, error) {
	prefix, err := filepath.Abs(location)
	if err != nil {
		return nil, err
	}
	ctx, cancelFunc := context.WithCancel(context.Background())
	eng := engine.CreateRuleEngine(ctx,
		10,
		log,
		engine.WithIncidentLimit(limitIncidents),
		engine.WithCodeSnipLimit(limitCodeSnips),
		engine.WithContextLines(contextLines),
		engine.WithIncidentSelector(incidentSelector),
		engine.WithLocationPrefixes([]string{prefix}),
	)

	// TODO: I am pretty sure that this should just be deleteod now.
	// this function already init's the java provider
	//jProvider, err := java.NewInternalProviderClient(ctx, log, contextLines, location, lspServerPath, bundles, depOpenSourceLabelsFile)
	//if err != nil {
	//cancelFunc()
	//	return nil, err
	//}

	bProvider, err := lib.GetProviderClient(provider.Config{Name: "builtin"}, log)
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
		"java":    jProvider,
		"builtin": bProvider,
	}

	parser := parser.RuleParser{
		ProviderNameToClient: providers,
		Log:                  log.WithName("parser"),
	}

	discoveryRulesets := []engine.RuleSet{}
	violationRulesets := []engine.RuleSet{}
	for _, f := range strings.Split(rules, ",") {
		internRuleSets, _, err := parser.LoadRules(strings.TrimSpace(f))
		if err != nil {
			log.Error(err, "unable to parse all the rules for ruleset", "file", f)
			cancelFunc()
			return nil, err
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

	log.Info("using rulesets", "discoverRulesets", len(discoveryRulesets), "violationRulesets", len(violationRulesets))
	// Generate discoveryRulesetCache here??

	return &analyzer{
		Logger:              log,
		engine:              eng,
		engineCtx:           ctx,
		cancelFunc:          cancelFunc,
		initedProviders:     providers,
		discoveryRulesets:   discoveryRulesets,
		violationRulesets:   violationRulesets,
		discoveryCache:      []konveyor.RuleSet{},
		discoveryCacheMutex: sync.Mutex{},
		cache:               NewIncidentsCache(log),
	}, nil

}
*/

func labelsContainDiscoveryOrAlways(labels []string) (bool, bool) {
	foundDiscoveryLabel := false
	foundIncludeAlways := false
	for _, label := range labels {
		if label == DISCOVERY_LABEL {
			foundDiscoveryLabel = true
		}
		if label == ALWAYS_INCLUDE_LABEL {
			foundIncludeAlways = true
		}
	}
	return foundDiscoveryLabel, foundIncludeAlways
}

// These will be the args that the client can use to tell the analyzer LSP what
// to do.
type Args struct {
	LabelSelector    string                 `json:"label_selector,omitempty"`
	IncidentSelector string                 `json:"incident_selector,omitempty"`
	IncludedPaths    []string               `json:"included_paths,omitempty"`
	ExcludedPaths    []string               `json:"excluded_paths,omitempty"`
	ResetCache       bool                   `json:"reset_cache,omitempty"`
	Carrier          propagation.MapCarrier `json:"carrier,omitempty"`
	// RulesFiles       []string
}

type Response struct {
	Rulesets []konveyor.RuleSet
}

func (a *analyzer) Stop() {
	a.Logger.Info("stopping engine")
	a.engine.Stop()
	a.Logger.Info("engine stopped")

	for providerName, provider := range a.initedProviders {
		a.Logger.Info("stopping provider", "provider", providerName)
		provider.Stop()
	}
}

func (a *analyzer) Analyze(client *rpc.Client, args Args, response *Response) error {
	prop := otel.GetTextMapPropagator()
	ctx := prop.Extract(context.Background(), args.Carrier)
	ctx, span := tracer.Start(ctx, "analyze")
	defer span.End()

	dRulesets, vRulesets := a.discoveryRulesets, a.violationRulesets
	if a.updateConditionProvider != nil {
		// TODO: This needs to be added back, but I am pretty sure that it was not not working
		/*var err error
		dRulesets, vRulesets, err = a.updateConditionProvider(client, a.initedProviders, a.discoveryRulesets, a.violationRulesets, a.Logger.WithName("provider update"), a.contextLines, a.location, a.rules)
		if err != nil {
			a.Logger.Error(err, "unable to update Conditions with new client")
			return err
		}*/
		a.Logger.Info("updated rulesets", "discovery", len(a.discoveryRulesets), "violations", len(a.violationRulesets))
	}

	//a.Logger.Info("compare before after", "before", fmt.Sprintf("%+v", a.violationRulesets), "after", fmt.Sprintf("%+v", vRulesets))

	selectors := []engine.RuleSelector{}
	if args.LabelSelector != "" {
		selector, err := labels.NewLabelSelector[*engine.RuleMeta](args.LabelSelector, nil)
		if err != nil {
			a.Logger.Error(err, "failed to create label selector from expression", "selector", args.LabelSelector)
			return err
		}
		selectors = append(selectors, selector)
	}
	a.Logger.Info("Have selectors", "selectors", selectors)

	scopes := []engine.Scope{}
	if len(args.IncludedPaths) > 0 {
		currScope := engine.IncludedPathsScope(args.IncludedPaths, a.Logger)
		scopes = append(scopes, currScope)
		a.Logger.V(2).Info("Using inclusion scope", "scope", currScope.Name())
	}

	// If we don't have scopes to test a single thing, and we don't have a reset cache request
	// Then we should return early, with results from the cache
	if len(scopes) == 0 && !args.ResetCache {
		a.Logger.Info("no scopes and not resetting cache, return early with results from cache")
		a.Logger.Info("Current cache len", a.cache.Len())
		response.Rulesets = a.createRulesetsFromCache()
		return nil
	}

	// Only exclude paths after we determine if we are going to run rules
	if len(args.ExcludedPaths) > 0 {
		currScope := engine.ExcludedPathsScope(args.ExcludedPaths, a.Logger)
		scopes = append(scopes, currScope)
		a.Logger.V(2).Info("Using exclusion scope", "scope", currScope.Name())
	}

	// Adding spans to the discovery rules run and for the violation rules run
	// to determine if discovery rule segmentation saves us enough
	if len(dRulesets) != 0 && args.ResetCache {
		// Here we want to refresh the discovery ruleset cache
		// Engine will emit per-rule progress automatically
		ctx, span := tracer.Start(ctx, "discovery-rules")
		rulesets := a.engine.RunRulesScopedWithOptions(ctx, dRulesets, engine.NewScope(scopes...),
			[]engine.RunOption{engine.WithProgressReporter(a.progressReporter)}, selectors...)
		a.discoveryCacheMutex.Lock()
		a.discoveryCache = rulesets
		a.discoveryCacheMutex.Unlock()
		span.End()
	}
	scopes = append(scopes, scope.NewDiscoveryRuleScope(a.Logger, a.discoveryCache))

	// This will already wait
	// Engine will emit per-rule progress automatically
	violationCTX, violationSpan := tracer.Start(ctx, "violation-rules")
	rulesets := a.engine.RunRulesScopedWithOptions(violationCTX, vRulesets, engine.NewScope(scopes...),
		[]engine.RunOption{engine.WithProgressReporter(a.progressReporter)}, selectors...)
	violationSpan.End()

	sort.SliceStable(rulesets, func(i, j int) bool {
		return rulesets[i].Name < rulesets[j].Name
	})

	a.Logger.Info("got rulesets", "rulesets", rulesets)

	// This is a full run, set the complete new results
	if len(args.IncludedPaths) == 0 {
		a.Logger.V(5).Info("setting cache for full run")
		a.setCache(rulesets)
	} else {
		a.Logger.V(5).Info("updating cache for filepath", "paths", args.IncludedPaths)
		a.updateCache(rulesets, args.IncludedPaths)
	}

	// Now we need to invalidate anything, from the files in included paths
	response.Rulesets = a.createRulesetsFromCache()

	// Report analysis complete
	a.progressReporter.Report(progress.ProgressEvent{
		Stage: progress.StageComplete,
	})

	return nil
}

func (a *analyzer) NotifyFileChanges(client *rpc.Client, args NotifyFileChangesArgs, response *NotifyFileChangesResponse) error {
	errs := []error{}
	for name, svcClient := range a.initedProviders {
		err := svcClient.NotifyFileChanges(context.Background(), args.Changes...)
		if err != nil {
			errs = append(errs, err)
		}
		a.Logger.Info("[pg] sent notify request", "name", name)
	}
	response.err = errors.Join(errs...)
	return nil
}

func (a *analyzer) setCache(rulesets []konveyor.RuleSet) {
	a.cache = NewIncidentsCache(a.Logger)
	a.addRulesetsToCache(rulesets)
}

func (a *analyzer) updateCache(rulesets []konveyor.RuleSet, includedPaths []string) {
	if includedPaths != nil {
		a.invalidateCachePerFile(includedPaths)
	}
	a.addRulesetsToCache(rulesets)
}

func (a *analyzer) addRulesetsToCache(rulesets []konveyor.RuleSet) {
	for _, r := range rulesets {
		for violationName, v := range r.Violations {
			for _, i := range v.Incidents {
				a.Logger.Info("here update cache incident", "incident", i)
				a.cache.Add(i.URI.Filename(), CacheValue{
					Incident: i,
					Violation: konveyor.Violation{
						Description: v.Description,
						Category:    v.Category,
						Labels:      v.Labels,
					},
					ViolationName: violationName,
					Ruleset: konveyor.RuleSet{
						Name:        r.Name,
						Description: r.Description,
						Tags:        r.Tags,
						Unmatched:   r.Unmatched,
						Skipped:     r.Skipped,
						Errors:      r.Errors,
					},
				})
			}
		}
	}
}

func (a *analyzer) invalidateCachePerFile(paths []string) {
	for _, p := range paths {
		a.Logger.Info("deleting cache entry for path", "path", p)
		a.cache.Delete(p)
	}
}

func (a *analyzer) createRulesetsFromCache() []konveyor.RuleSet {
	ruleSetMap := map[string]konveyor.RuleSet{}
	a.Logger.V(8).Info("cache", "cacheVal", a.cache)
	for filePath, cacheValue := range a.cache.Entries() {
		for _, v := range cacheValue {
			if ruleset, ok := ruleSetMap[v.Ruleset.Name]; ok {
				if vio, ok := ruleset.Violations[v.ViolationName]; ok {
					vio.Incidents = append(vio.Incidents, v.Incident)
					ruleset.Violations[v.ViolationName] = vio
					ruleSetMap[ruleset.Name] = ruleset
				} else {
					violation := v.Violation
					violation.Incidents = []konveyor.Incident{v.Incident}
					ruleset.Violations[v.ViolationName] = violation
					ruleSetMap[ruleset.Name] = ruleset
				}
			} else {
				violation := v.Violation
				violation.Incidents = []konveyor.Incident{v.Incident}
				ruleset := v.Ruleset
				ruleset.Violations = map[string]konveyor.Violation{
					v.ViolationName: violation,
				}
				ruleSetMap[ruleset.Name] = ruleset
			}
		}
		a.Logger.V(8).Info("ruleset from cacheValue", "rulesets", ruleSetMap, "filePath", filePath)
	}

	r := []konveyor.RuleSet{}
	for _, ruleset := range ruleSetMap {
		r = append(r, ruleset)
	}
	a.Logger.V(8).Info("ruleset from cache", "rulesets", r)
	return r
}
