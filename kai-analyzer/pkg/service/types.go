package service

import "github.com/konveyor/analyzer-lsp/output/v1/konveyor"

type InitializeArgs struct {
	Workers          int        `json:"workers"`
	LimitIncidents   int        `json:"limit_incidents"`
	LimitCodeSnips   int        `json:"limit_code_snips"`
	ContextLines     int        `json:"context_lines"`
	Location         string     `json:"location"`
	IncidentSelector string     `json:"incident_selector"`
	RuleFiles        []string   `json:"rule_files"`
	JavaConfig       JavaConfig `json:"java_config"`
	AnalysisMode     string     `json:"analysis_mode"`
}

type JavaConfig struct {
	Bundles       string `json:"bundles"`
	LSPServerPath string `json:"lspServerPath"`
}

type AnalyzeArgs struct {
	LabelSelector string   `json:"label_selector,omitempty"`
	IncludedPaths []string `json:"included_paths,omitempty"`
	RuleFiles     []string `json:"rule_files,omitempty"`
}

type AnalyzeResponse struct {
	Rulesets []konveyor.RuleSet
}
