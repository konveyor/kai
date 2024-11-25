package service

import (
	"context"
	"sort"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/engine/labels"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/parser"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"
	"github.com/konveyor/kai-analyzer/provider/java"
)

type Analyzer struct {
	Logger logr.Logger

	engine     engine.RuleEngine
	engineCtx  context.Context
	cancelFunc context.CancelFunc

	initedProviders map[string]provider.InternalProviderClient
	ruleSets        []engine.RuleSet
}

func NewAnalyzer(limitIncidents, limitCodeSnips, contextLines int, location, incidentSelector, lspServerPath, bundles, depOpenSourceLabelsFile string, ruleFiles []string, log logr.Logger) (*Analyzer, error) {
	ctx, cancelFunc := context.WithCancel(context.Background())
	eng := engine.CreateRuleEngine(ctx,
		10,
		log,
		engine.WithIncidentLimit(limitIncidents),
		engine.WithCodeSnipLimit(limitCodeSnips),
		engine.WithContextLines(contextLines),
		engine.WithIncidentSelector(incidentSelector),
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
	for _, f := range ruleFiles {
		internRuleSet, _, err := parser.LoadRules(f)
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
		initedProviders: map[string]provider.InternalProviderClient{},
		ruleSets:        ruleSets,
	}, nil

}

// These will be the args that the client can use to tell the anlayzer LSP what to do.
type Args struct {
	LabelSelector    string   `json:"label_selector,omitempty"`
	IncidentSelector string   `json:"incident_selector,omitempty"`
	IncludedPaths    []string `json:"included_paths,omitempty"`
	// RulesFiles       []string
}

type Response struct {
	Rulesets []konveyor.RuleSet
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

	// This will already wait
	rulesets := a.engine.RunRules(context.Background(), a.ruleSets, selectors...)

	sort.SliceStable(rulesets, func(i, j int) bool {
		return rulesets[i].Name < rulesets[j].Name
	})

	response.Rulesets = rulesets
	return nil
}
