package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
	progressreporter "github.com/konveyor/analyzer-lsp/progress/reporter"
)

func TestCreateProgressReporter_Noop(t *testing.T) {
	// When no output specified, should return NoopReporter
	reporter, cleanup := createProgressReporter("", "json", logr.Discard())
	defer cleanup()

	if reporter == nil {
		t.Fatal("Expected non-nil reporter")
	}

	// NoopReporter should not panic when reporting
	reporter.Report(progress.Event{
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
	reporter.Report(progress.Event{
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
	reporter := progressreporter.NewJSONReporter(&buf)

	event := progress.Event{
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
	var parsed progress.Event
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
	reporter := progressreporter.NewTextReporter(&buf)

	event := progress.Event{
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
	reporter := progressreporter.NewJSONReporter(&buf)

	stages := []progress.Stage{
		progress.StageInit,
		progress.StageProviderInit,
		progress.StageRuleParsing,
		progress.StageRuleExecution,
		progress.StageComplete,
	}

	for _, stage := range stages {
		reporter.Report(progress.Event{
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
		var event progress.Event
		if err := json.Unmarshal([]byte(line), &event); err != nil {
			t.Errorf("Line %d: failed to parse JSON: %v", i, err)
		}
	}
}

// logLines writes one debug, info and error message through a handler built
// by newLogHandler and returns the messages that reached the log file.
func logLines(t *testing.T, verbosity int) []string {
	t.Helper()
	path := filepath.Join(t.TempDir(), "kai.log")
	handler, closeLog, err := newLogHandler(path, verbosity)
	if err != nil {
		t.Fatalf("newLogHandler: %v", err)
	}
	l := logr.FromSlogHandler(handler)
	l.V(1).Info("debug message")
	l.Info("info message")
	l.Error(errors.New("boom"), "error message")
	closeLog()

	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("reading log file: %v", err)
	}
	var msgs []string
	for _, line := range strings.Split(strings.TrimSpace(string(data)), "\n") {
		if line == "" {
			continue
		}
		var entry struct {
			Msg string `json:"msg"`
		}
		if err := json.Unmarshal([]byte(line), &entry); err != nil {
			t.Fatalf("log line is not JSON: %q: %v", line, err)
		}
		msgs = append(msgs, entry.Msg)
	}
	return msgs
}

func TestNewLogHandler_HonorsVerbosity(t *testing.T) {
	tests := []struct {
		name      string
		verbosity int
		want      []string
	}{
		{"debug", -4, []string{"debug message", "info message", "error message"}},
		{"info", 0, []string{"info message", "error message"}},
		{"warning", 4, []string{"error message"}},
		{"error", 8, []string{"error message"}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := logLines(t, tt.verbosity)
			if strings.Join(got, "|") != strings.Join(tt.want, "|") {
				t.Errorf("verbosity %d logged %v, want %v", tt.verbosity, got, tt.want)
			}
		})
	}
}

func TestNewLogHandler_StderrWhenNoLogFile(t *testing.T) {
	handler, closeLog, err := newLogHandler("", 0)
	if err != nil {
		t.Fatalf("newLogHandler: %v", err)
	}
	defer closeLog()
	if handler == nil {
		t.Fatal("Expected a handler writing to stderr")
	}
}

func TestNewLogHandler_UnwritableLogFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "missing-dir", "kai.log")
	if _, _, err := newLogHandler(path, 0); err == nil {
		t.Fatal("Expected an error for a log file in a missing directory")
	}
}

func TestVersionString(t *testing.T) {
	origVersion, origCommit := version, commit
	defer func() { version, commit = origVersion, origCommit }()

	version, commit = "v1.2.3", "abc123"
	got := versionString()
	if got != "version: v1.2.3\ncommit: abc123" {
		t.Errorf("unexpected version string %q", got)
	}

	commit = ""
	if got := resolvedCommit(); got == "" {
		t.Error("Expected a fallback commit value when none was injected")
	}
}

// TestVersionFlag builds the real binary with injected build variables and
// checks that -version prints them without starting the server.
func TestVersionFlag(t *testing.T) {
	bin := filepath.Join(t.TempDir(), "kai-analyzer")
	build := exec.Command("go", "build",
		"-ldflags", "-X main.version=v9.9.9 -X main.commit=deadbeef",
		"-o", bin, ".")
	if out, err := build.CombinedOutput(); err != nil {
		t.Fatalf("go build failed: %v\n%s", err, out)
	}

	out, err := exec.Command(bin, "-version").Output()
	if err != nil {
		t.Fatalf("running -version: %v", err)
	}
	got := string(out)
	if !strings.Contains(got, "version: v9.9.9") || !strings.Contains(got, "commit: deadbeef") {
		t.Errorf("unexpected -version output %q", got)
	}
}
