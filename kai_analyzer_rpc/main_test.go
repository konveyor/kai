package main

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
)

func TestCreateProgressReporter_Noop(t *testing.T) {
	// When no output specified, should return NoopReporter
	reporter, cleanup := createProgressReporter("", "json", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter")
	}

	// NoopReporter should not panic when reporting
	reporter.Report(progress.ProgressEvent{
		Stage: progress.StageInit,
	})
}

func TestCreateProgressReporter_JSON_Stderr(t *testing.T) {
	// Should create JSON reporter for stderr
	reporter, cleanup := createProgressReporter("stderr", "json", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter")
	}
}

func TestCreateProgressReporter_JSON_Stdout(t *testing.T) {
	// Should create JSON reporter for stdout
	reporter, cleanup := createProgressReporter("stdout", "json", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter")
	}
}

func TestCreateProgressReporter_Text(t *testing.T) {
	// Should create text reporter when format is text
	reporter, cleanup := createProgressReporter("stderr", "text", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter")
	}
}

func TestCreateProgressReporter_File(t *testing.T) {
	// Should create reporter that writes to file
	tmpFile := filepath.Join(os.TempDir(), "kai-progress-test.json")
	defer os.Remove(tmpFile)

	reporter, cleanup := createProgressReporter(tmpFile, "json", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter")
	}

	// Report an event
	reporter.Report(progress.ProgressEvent{
		Stage: progress.StageInit,
	})

	// Verify file was created
	if _, err := os.Stat(tmpFile); os.IsNotExist(err) {
		t.Fatalf("Expected file to be created at %s", tmpFile)
	}
}

func TestCreateProgressReporter_InvalidFile(t *testing.T) {
	// Should fallback to stderr when file creation fails
	reporter, cleanup := createProgressReporter("/invalid/path/file.json", "json", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter (should fallback to stderr)")
	}
}

func TestProgressReporter_JSONFormat(t *testing.T) {
	// Test that JSON reporter produces valid JSON
	var buf bytes.Buffer
	reporter := progress.NewJSONReporter(&buf)

	event := progress.ProgressEvent{
		Stage:   progress.StageRuleExecution,
		Current: 23,
		Total:   45,
		Message: "test-rule",
	}

	reporter.Report(event)

	output := buf.String()
	if output == "" {
		t.Fatal("Expected JSON output, got empty string")
	}

	// Verify it's valid JSON
	var parsed progress.ProgressEvent
	lines := strings.Split(strings.TrimSpace(output), "\n")
	if err := json.Unmarshal([]byte(lines[0]), &parsed); err != nil {
		t.Fatalf("Failed to parse JSON: %v\nOutput: %s", err, output)
	}

	// Verify fields
	if parsed.Stage != progress.StageRuleExecution {
		t.Errorf("Expected stage %s, got %s", progress.StageRuleExecution, parsed.Stage)
	}

	if parsed.Current != 23 {
		t.Errorf("Expected current 23, got %d", parsed.Current)
	}

	if parsed.Total != 45 {
		t.Errorf("Expected total 45, got %d", parsed.Total)
	}

	// Verify percent was auto-calculated
	if parsed.Percent == 0.0 {
		t.Error("Expected percent to be auto-calculated")
	}

	expectedPercent := float64(23) / float64(45) * 100.0
	tolerance := 0.01
	if parsed.Percent < expectedPercent-tolerance || parsed.Percent > expectedPercent+tolerance {
		t.Errorf("Expected percent ~%.2f, got %.2f", expectedPercent, parsed.Percent)
	}
}

func TestProgressReporter_TextFormat(t *testing.T) {
	// Test that text reporter produces human-readable output
	var buf bytes.Buffer
	reporter := progress.NewTextReporter(&buf)

	event := progress.ProgressEvent{
		Stage:   progress.StageRuleExecution,
		Current: 23,
		Total:   45,
	}

	reporter.Report(event)

	output := buf.String()
	if output == "" {
		t.Fatal("Expected text output, got empty string")
	}

	// Verify output contains expected strings
	if !strings.Contains(output, "23/45") {
		t.Errorf("Expected '23/45' in output, got: %s", output)
	}
}

func TestProgressReporter_AllStages(t *testing.T) {
	// Test that all stages can be reported without errors
	var buf bytes.Buffer
	reporter := progress.NewJSONReporter(&buf)

	stages := []progress.Stage{
		progress.StageInit,
		progress.StageProviderInit,
		progress.StageRuleParsing,
		progress.StageRuleExecution,
		progress.StageComplete,
	}

	for _, stage := range stages {
		reporter.Report(progress.ProgressEvent{
			Stage: stage,
		})
	}

	output := buf.String()
	lines := strings.Split(strings.TrimSpace(output), "\n")

	if len(lines) != len(stages) {
		t.Errorf("Expected %d events, got %d", len(stages), len(lines))
	}

	// Verify each line is valid JSON
	for i, line := range lines {
		var event progress.ProgressEvent
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			t.Errorf("Line %d: failed to parse JSON: %v", i, err)
		}
	}
}
