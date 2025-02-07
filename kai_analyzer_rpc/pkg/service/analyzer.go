package service

import (
	"context"
	"path/filepath"
	"sort"
	"strings"
	"sync"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/engine/labels"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/parser"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"
	"github.com/konveyor/kai-analyzer/provider/java"
)

type cacheValue struct {
	incident      konveyor.Incident
	ViolationName string
	violation     konveyor.Violation
	ruleset       konveyor.RuleSet
}

type Analyzer struct {
	Logger logr.Logger

	engine     engine.RuleEngine
	engineCtx  context.Context
	cancelFunc context.CancelFunc

	initedProviders map[string]provider.InternalProviderClient
	ruleSets        []engine.RuleSet

	cache      map[string][]cacheValue
	cacheMutex sync.RWMutex
}

func NewAnalyzer(limitIncidents, limitCodeSnips, contextLines int, location, incidentSelector, lspServerPath, bundles, depOpenSourceLabelsFile, rules string, log logr.Logger) (*Analyzer, error) {
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

	// this function already init's the java provider
	jProvider, err := java.NewInternalProviderClient(ctx, log, contextLines, location, lspServerPath, bundles, depOpenSourceLabelsFile)
	if err != nil {
		cancelFunc()
		return nil, err
	}

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

	ruleSets := []engine.RuleSet{}
	for _, f := range strings.Split(rules, ",") {
		internRuleSet, _, err := parser.LoadRules(strings.TrimSpace(f))
		if err != nil {
			log.Error(err, "unable to parse all the rules for ruleset", "file", f)
			cancelFunc()
			return nil, err
		}
		ruleSets = append(ruleSets, internRuleSet...)
	}

	return &Analyzer{
		Logger:          log,
		engine:          eng,
		engineCtx:       ctx,
		cancelFunc:      cancelFunc,
		initedProviders: providers,
		ruleSets:        ruleSets,
		cache:           map[string][]cacheValue{},
		cacheMutex:      sync.RWMutex{},
	}, nil

}

// These will be the args that the client can use to tell the analyzer LSP what
// to do.
type Args struct {
	LabelSelector    string   `json:"label_selector,omitempty"`
	IncidentSelector string   `json:"incident_selector,omitempty"`
	IncludedPaths    []string `json:"included_paths,omitempty"`
	ExcludedPaths    []string `json:"excluded_paths,omitempty"`
	// RulesFiles       []string
}

type Response struct {
	Rulesets []konveyor.RuleSet
}

func (a *Analyzer) Stop() {
	a.Logger.Info("stopping engine")
	a.engine.Stop()
	a.Logger.Info("engine stopped")

	for providerName, provider := range a.initedProviders {
		a.Logger.Info("stopping provider", "provider", providerName)
		provider.Stop()
	}
}

func (a *Analyzer) Analyze(args Args, response *Response) error {
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

	if len(args.ExcludedPaths) > 0 {
		currScope := engine.ExcludedPathsScope(args.ExcludedPaths, a.Logger)
		scopes = append(scopes, currScope)
		a.Logger.V(2).Info("Using exclusion scope", "scope", currScope.Name())
	}

	// This will already wait
	rulesets := a.engine.RunRulesScoped(context.Background(), a.ruleSets, engine.NewScope(scopes...), selectors...)

	sort.SliceStable(rulesets, func(i, j int) bool {
		return rulesets[i].Name < rulesets[j].Name
	})

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
	return nil
}

func (a *Analyzer) setCache(rulesets []konveyor.RuleSet) {
	a.cacheMutex.Lock()
	defer a.cacheMutex.Unlock()
	a.cache = map[string][]cacheValue{}

	a.addRulesetsToCache(rulesets)
}

func (a *Analyzer) updateCache(rulesets []konveyor.RuleSet, includedPaths []string) {
	a.cacheMutex.Lock()
	defer a.cacheMutex.Unlock()
	if includedPaths != nil {
		a.invalidateCachePerFile(includedPaths)
	}
	a.addRulesetsToCache(rulesets)
}

func (a *Analyzer) addRulesetsToCache(rulesets []konveyor.RuleSet) {

	for _, r := range rulesets {
		for violationName, v := range r.Violations {
			for _, i := range v.Incidents {
				a.Logger.V(8).Info("here update cache incident", "incident", i)
				if l, ok := a.cache[i.URI.Filename()]; ok {
					l = append(l, cacheValue{
						incident: i,
						violation: konveyor.Violation{
							Description: v.Description,
							Category:    v.Category,
							Labels:      v.Labels,
						},
						ViolationName: violationName,
						ruleset: konveyor.RuleSet{
							Name:        r.Name,
							Description: r.Description,
							Tags:        r.Tags,
							Unmatched:   r.Unmatched,
							Skipped:     r.Skipped,
							Errors:      r.Errors,
						},
					})
					a.cache[i.URI.Filename()] = l
				} else {
					a.cache[i.URI.Filename()] = []cacheValue{{
						incident: i,
						violation: konveyor.Violation{
							Description: v.Description,
							Category:    v.Category,
							Labels:      v.Labels,
						},
						ViolationName: violationName,
						ruleset: konveyor.RuleSet{
							Name:        r.Name,
							Description: r.Description,
							Tags:        r.Tags,
							Unmatched:   r.Unmatched,
							Skipped:     r.Skipped,
							Errors:      r.Errors,
						},
					}}
				}
			}
		}
	}
}

func (a *Analyzer) invalidateCachePerFile(paths []string) {
	for _, p := range paths {
		a.Logger.Info("deleting cache entry for path", "path", p)
		delete(a.cache, p)
	}
}

func (a *Analyzer) createRulesetsFromCache() []konveyor.RuleSet {
	a.cacheMutex.RLock()
	defer a.cacheMutex.RUnlock()

	ruleSetMap := map[string]konveyor.RuleSet{}
	a.Logger.V(8).Info("cache", "cacheVal", a.cache)
	for filePath, cacheValue := range a.cache {
		for _, v := range cacheValue {

			if ruleset, ok := ruleSetMap[v.ruleset.Name]; ok {
				if vio, ok := ruleset.Violations[v.ViolationName]; ok {
					vio.Incidents = append(vio.Incidents, v.incident)
					ruleset.Violations[v.ViolationName] = vio
					ruleSetMap[ruleset.Name] = ruleset
				} else {
					violation := v.violation
					violation.Incidents = []konveyor.Incident{v.incident}
					ruleset.Violations[v.ViolationName] = violation
					ruleSetMap[ruleset.Name] = ruleset
				}
			} else {
				violation := v.violation
				violation.Incidents = []konveyor.Incident{v.incident}
				ruleset := v.ruleset
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
