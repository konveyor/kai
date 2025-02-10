package scope

import (
	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
)

type DiscoveryRuleScope struct {
	log      logr.Logger
	rulesets []konveyor.RuleSet
}

func NewDiscoveryRuleScope(log logr.Logger, rulesets []konveyor.RuleSet) engine.Scope {
	return &DiscoveryRuleScope{
		log:      log,
		rulesets: rulesets,
	}
}

// AddToContext implements engine.Scope.
func (d *DiscoveryRuleScope) AddToContext(condctx *engine.ConditionContext) error {
	if condctx.Tags == nil {
		condctx.Tags = map[string]interface{}{}
	}
	d.log.Info("Adding tags to condctx", "condctx", condctx)
	for _, ruleset := range d.rulesets {
		for _, tag := range ruleset.Tags {
			if _, ok := condctx.Tags[tag]; !ok {
				d.log.V(2).Info("adding tag", "tag", tag)
				condctx.Tags[tag] = true
			}
		}
	}
	return nil
}

// FilterResponse implements engine.Scope.
func (d *DiscoveryRuleScope) FilterResponse(engine.IncidentContext) bool {
	return false
}

// Name implements engine.Scope.
func (d *DiscoveryRuleScope) Name() string {
	return "DiscoveryRulesetsScopes"
}

var _ engine.Scope = &DiscoveryRuleScope{}
