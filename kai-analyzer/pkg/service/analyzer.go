package service

import (
	"context"
	"sort"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/engine/labels"
	"github.com/konveyor/analyzer-lsp/parser"
	"github.com/konveyor/analyzer-lsp/provider"
	"github.com/konveyor/analyzer-lsp/provider/lib"

	javaexp "github.com/konveyor/analyzer-lsp/external-providers/java-external-provider/pkg/java_external_provider"
)

type Analyzer struct {
	Logger logr.Logger

	engine     engine.RuleEngine
	engineCtx  context.Context
	cancelFunc context.CancelFunc

	initedProviders map[string]provider.InternalProviderClient
}

func NewAnalyzer(log logr.Logger) *Analyzer {
	return &Analyzer{
		Logger:          log,
		initedProviders: map[string]provider.InternalProviderClient{},
	}
}

func (a *Analyzer) Initialize(args InitializeArgs) error {
	ctx, cancelFunc := context.WithCancel(context.Background())
	eng := engine.CreateRuleEngine(ctx,
		args.Workers,
		a.Logger,
		engine.WithIncidentLimit(args.LimitIncidents),
		engine.WithCodeSnipLimit(args.LimitCodeSnips),
		engine.WithContextLines(args.ContextLines),
		engine.WithIncidentSelector(args.IncidentSelector),
	)

	javaProvider := javaexp.NewJavaProvider(a.Logger, "java", args.ContextLines, provider.Config{Name: "java"})
	_, _, err := javaProvider.Init(ctx, a.Logger, provider.InitConfig{
		Location: args.Location,
		ProviderSpecificConfig: map[string]interface{}{
			"lspServerName": "java",
			"bundles":       args.JavaConfig.Bundles,
			"lspServerPath": args.JavaConfig.LSPServerPath,
		},
		Proxy:        &provider.Proxy{},
		AnalysisMode: provider.AnalysisMode(args.AnalysisMode),
	})
	if err != nil {
		cancelFunc()
		return err
	}
	_, err = javaProvider.ProviderInit(ctx, []provider.InitConfig{})
	if err != nil {
		cancelFunc()
		return err
	}
	a.initedProviders["java"] = javaProvider

	builtinProvider, err := lib.GetProviderClient(provider.Config{Name: "builtin"}, a.Logger)
	if err != nil {
		cancelFunc()
		return err
	}
	_, _, err = builtinProvider.Init(ctx, a.Logger, provider.InitConfig{})
	if err != nil {
		cancelFunc()
		return err
	}
	_, err = builtinProvider.ProviderInit(context.Background(), []provider.InitConfig{{Location: args.Location}})
	if err != nil {
		cancelFunc()
		return err
	}
	a.initedProviders["builtin"] = builtinProvider

	a.engine = eng
	a.engineCtx = ctx
	a.cancelFunc = cancelFunc

	return nil
}

func (a *Analyzer) Analyze(args AnalyzeArgs, response *AnalyzeResponse) error {

	parser := parser.RuleParser{
		ProviderNameToClient: a.initedProviders,
		Log:                  a.Logger.WithName("parser"),
		NoDependencyRules:    true,
	}

	ruleSets := []engine.RuleSet{}
	for _, f := range args.RuleFiles {
		internRuleSet, _, err := parser.LoadRules(f)
		if err != nil {
			a.Logger.Error(err, "unable to parse all the rules for ruleset", "file", f)
			a.cancelFunc()
			return err
		}
		ruleSets = append(ruleSets, internRuleSet...)
	}

	selectors := []engine.RuleSelector{}
	if args.LabelSelector != "" {
		selector, err := labels.NewLabelSelector[*engine.RuleMeta](args.LabelSelector, nil)
		if err != nil {
			a.Logger.Error(err, "failed to create label selector from expression", "selector", args.LabelSelector)
			return err
		}
		selectors = append(selectors, selector)
	}

	// This will already wait
	rulesets := a.engine.RunRules(context.Background(), ruleSets, selectors...)

	sort.SliceStable(rulesets, func(i, j int) bool {
		return rulesets[i].Name < rulesets[j].Name
	})

	response.Rulesets = rulesets
	return nil
}

func (a *Analyzer) Shutdown() {
	for _, provider := range a.initedProviders {
		provider.Stop()
	}
}

func (a *Analyzer) Exit() {}
