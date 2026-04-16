package service

import (
	"testing"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/engine"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
	"github.com/konveyor/analyzer-lsp/provider"
)

func TestAnalyzer_Providers(t *testing.T) {
	providers := map[string]provider.InternalProviderClient{
		"java":    nil, // we don't need real clients to test the getter
		"builtin": nil,
	}

	a := &analyzer{
		Logger:          logr.Discard(),
		initedProviders: providers,
	}

	got := a.Providers()
	if len(got) != 2 {
		t.Fatalf("expected 2 providers, got %d", len(got))
	}
	if _, ok := got["java"]; !ok {
		t.Error("expected 'java' provider")
	}
	if _, ok := got["builtin"]; !ok {
		t.Error("expected 'builtin' provider")
	}

	// Verify defensive copy — mutating returned map should not affect internal state
	delete(got, "java")
	if len(a.initedProviders) != 2 {
		t.Error("mutating returned map should not affect internal providers")
	}
}

func TestAnalyzer_RuleSets(t *testing.T) {
	discovery := []engine.RuleSet{
		{Name: "discovery-1"},
	}
	violation := []engine.RuleSet{
		{Name: "violation-1"},
		{Name: "violation-2"},
	}

	a := &analyzer{
		Logger:            logr.Discard(),
		discoveryRulesets: discovery,
		violationRulesets: violation,
	}

	gotDiscovery, gotViolation := a.RuleSets()
	if len(gotDiscovery) != 1 {
		t.Fatalf("expected 1 discovery ruleset, got %d", len(gotDiscovery))
	}
	if gotDiscovery[0].Name != "discovery-1" {
		t.Errorf("expected discovery ruleset name 'discovery-1', got '%s'", gotDiscovery[0].Name)
	}
	if len(gotViolation) != 2 {
		t.Fatalf("expected 2 violation rulesets, got %d", len(gotViolation))
	}
	if gotViolation[0].Name != "violation-1" {
		t.Errorf("expected violation ruleset name 'violation-1', got '%s'", gotViolation[0].Name)
	}

	// Verify defensive copy — mutating returned elements should not affect internals
	gotDiscovery[0].Name = "mutated"
	if a.discoveryRulesets[0].Name == "mutated" {
		t.Error("mutating returned slice should not affect internal discovery rulesets")
	}
}

func TestAnalyzer_Cache(t *testing.T) {
	cache := NewIncidentsCache(logr.Discard())
	cache.Add("/test/file.java", CacheValue{
		Incident:      konveyor.Incident{Message: "test incident"},
		ViolationName: "test-violation",
	})

	a := &analyzer{
		Logger: logr.Discard(),
		cache:  cache,
	}

	got := a.Cache()
	if got == nil {
		t.Fatal("expected non-nil cache")
	}
	if got.Len() != 1 {
		t.Errorf("expected cache length 1, got %d", got.Len())
	}
	entries, ok := got.Get("/test/file.java")
	if !ok {
		t.Fatal("expected cache entry for /test/file.java")
	}
	if len(entries) != 1 {
		t.Fatalf("expected 1 cache entry, got %d", len(entries))
	}
	if entries[0].ViolationName != "test-violation" {
		t.Errorf("expected violation name 'test-violation', got '%s'", entries[0].ViolationName)
	}

	// Verify defensive copy — mutating returned cache should not affect internals
	got.Delete("/test/file.java")
	if a.cache.Len() != 1 {
		t.Error("mutating returned cache should not affect internal cache")
	}
}

func TestAnalyzer_CachedRuleSets(t *testing.T) {
	cache := NewIncidentsCache(logr.Discard())

	// Add incidents for two different rulesets
	cache.Add("/test/file1.java", CacheValue{
		Incident:      konveyor.Incident{Message: "incident 1"},
		ViolationName: "viol-1",
		Violation: konveyor.Violation{
			Description: "violation 1 desc",
		},
		Ruleset: konveyor.RuleSet{
			Name:        "ruleset-A",
			Description: "Ruleset A",
		},
	})
	cache.Add("/test/file2.java", CacheValue{
		Incident:      konveyor.Incident{Message: "incident 2"},
		ViolationName: "viol-2",
		Violation: konveyor.Violation{
			Description: "violation 2 desc",
		},
		Ruleset: konveyor.RuleSet{
			Name:        "ruleset-B",
			Description: "Ruleset B",
		},
	})

	a := &analyzer{
		Logger: logr.Discard(),
		cache:  cache,
	}

	got := a.CachedRuleSets()
	if len(got) != 2 {
		t.Fatalf("expected 2 rulesets, got %d", len(got))
	}

	// Build a map for easier assertion (order is not guaranteed)
	rulesetMap := map[string]konveyor.RuleSet{}
	for _, rs := range got {
		rulesetMap[rs.Name] = rs
	}

	rsA, ok := rulesetMap["ruleset-A"]
	if !ok {
		t.Fatal("expected 'ruleset-A' in cached rulesets")
	}
	if len(rsA.Violations) != 1 {
		t.Fatalf("expected 1 violation in ruleset-A, got %d", len(rsA.Violations))
	}
	if v, ok := rsA.Violations["viol-1"]; !ok {
		t.Error("expected 'viol-1' violation in ruleset-A")
	} else if len(v.Incidents) != 1 {
		t.Errorf("expected 1 incident in viol-1, got %d", len(v.Incidents))
	}

	rsB, ok := rulesetMap["ruleset-B"]
	if !ok {
		t.Fatal("expected 'ruleset-B' in cached rulesets")
	}
	if len(rsB.Violations) != 1 {
		t.Fatalf("expected 1 violation in ruleset-B, got %d", len(rsB.Violations))
	}
}

func TestAnalyzer_CachedRuleSets_Empty(t *testing.T) {
	cache := NewIncidentsCache(logr.Discard())

	a := &analyzer{
		Logger: logr.Discard(),
		cache:  cache,
	}

	got := a.CachedRuleSets()
	if len(got) != 0 {
		t.Errorf("expected 0 rulesets from empty cache, got %d", len(got))
	}
}

// TestAnalyzerInterface_HasExportedMethods verifies that the Analyzer interface
// includes the 4 new exported methods. This is a compile-time check — if the
// interface doesn't include these methods, this test won't compile.
func TestAnalyzerInterface_HasExportedMethods(t *testing.T) {
	var a Analyzer
	// This function uses the Analyzer interface to verify
	// the exported methods exist. If any are missing, this
	// won't compile.
	_ = func(analyzer Analyzer) {
		analyzer.Providers()
		analyzer.RuleSets()
		analyzer.Cache()
		analyzer.CachedRuleSets()
	}
	_ = a
}
