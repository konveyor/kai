package service

import (
	"errors"
	"sync"
	"testing"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
)

// mockRPCNotifier is a mock RPC notifier for testing
type mockRPCNotifier struct {
	notifications []notificationCall
	mu            sync.Mutex
	notifyError   error
}

type notificationCall struct {
	method string
	args   interface{}
}

func (m *mockRPCNotifier) Notify(method string, args interface{}) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.notifications = append(m.notifications, notificationCall{
		method: method,
		args:   args,
	})
	return m.notifyError
}

func (m *mockRPCNotifier) getNotifications() []notificationCall {
	m.mu.Lock()
	defer m.mu.Unlock()
	return append([]notificationCall{}, m.notifications...)
}

// newRPCProgressReporterForTest creates an RPC progress reporter for testing.
// This bypasses the NewRPCProgressReporter constructor to allow passing a mock.
func newRPCProgressReporterForTest(notifier RPCNotifier, logger logr.Logger) progress.ProgressReporter {
	return &RPCProgressReporter{
		notifier: notifier,
		logger:   logger,
	}
}

func TestRPCProgressReporter_Report(t *testing.T) {
	// Create a mock notifier
	mockNotifier := &mockRPCNotifier{}

	// Create RPC progress reporter
	reporter := newRPCProgressReporterForTest(mockNotifier, logr.Discard())

	// Report a progress event
	event := progress.ProgressEvent{
		Stage:   progress.StageInit,
		Message: "Starting analysis",
	}
	reporter.Report(event)

	// Verify the notification was sent
	notifications := mockNotifier.getNotifications()
	if len(notifications) != 1 {
		t.Fatalf("expected 1 notification, got %d", len(notifications))
	}

	if notifications[0].method != "analysis.progress" {
		t.Errorf("expected method 'analysis.progress', got '%s'", notifications[0].method)
	}

	// Verify the event was passed correctly
	if eventArg, ok := notifications[0].args.(progress.ProgressEvent); ok {
		if eventArg.Stage != progress.StageInit {
			t.Errorf("expected stage StageInit, got %s", eventArg.Stage)
		}
		if eventArg.Message != "Starting analysis" {
			t.Errorf("expected message 'Starting analysis', got '%s'", eventArg.Message)
		}
	} else {
		t.Errorf("expected ProgressEvent argument, got %T", notifications[0].args)
	}
}

func TestRPCProgressReporter_AllStages(t *testing.T) {
	// Create a mock notifier
	mockNotifier := &mockRPCNotifier{}

	// Create RPC progress reporter
	reporter := newRPCProgressReporterForTest(mockNotifier, logr.Discard())

	// Test all stages
	stages := []progress.Stage{
		progress.StageInit,
		progress.StageProviderInit,
		progress.StageRuleParsing,
		progress.StageRuleExecution,
		progress.StageComplete,
	}

	for _, stage := range stages {
		event := progress.ProgressEvent{
			Stage:   stage,
			Message: string(stage),
		}
		reporter.Report(event)
	}

	// Verify all notifications were sent
	notifications := mockNotifier.getNotifications()
	if len(notifications) != len(stages) {
		t.Fatalf("expected %d notifications, got %d", len(stages), len(notifications))
	}

	for i, notification := range notifications {
		if notification.method != "analysis.progress" {
			t.Errorf("notification %d: expected method 'analysis.progress', got '%s'", i, notification.method)
		}

		if eventArg, ok := notification.args.(progress.ProgressEvent); ok {
			if eventArg.Stage != stages[i] {
				t.Errorf("notification %d: expected stage %s, got %s", i, stages[i], eventArg.Stage)
			}
		}
	}
}

func TestRPCProgressReporter_WithProgress(t *testing.T) {
	// Create a mock notifier
	mockNotifier := &mockRPCNotifier{}

	// Create RPC progress reporter
	reporter := newRPCProgressReporterForTest(mockNotifier, logr.Discard())

	// Report progress event with current/total/percent
	event := progress.ProgressEvent{
		Stage:   progress.StageRuleExecution,
		Message: "Processing rule xyz",
		Current: 5,
		Total:   10,
		Percent: 50.0,
	}
	reporter.Report(event)

	// Verify the notification was sent with all fields
	notifications := mockNotifier.getNotifications()
	if len(notifications) != 1 {
		t.Fatalf("expected 1 notification, got %d", len(notifications))
	}

	if eventArg, ok := notifications[0].args.(progress.ProgressEvent); ok {
		if eventArg.Current != 5 {
			t.Errorf("expected current 5, got %d", eventArg.Current)
		}
		if eventArg.Total != 10 {
			t.Errorf("expected total 10, got %d", eventArg.Total)
		}
		if eventArg.Percent != 50.0 {
			t.Errorf("expected percent 50.0, got %f", eventArg.Percent)
		}
	}
}

func TestRPCProgressReporter_NilNotifier(t *testing.T) {
	// Create reporter with nil notifier
	reporter := newRPCProgressReporterForTest(nil, logr.Discard())

	// Should not panic when reporting with nil client
	event := progress.ProgressEvent{
		Stage: progress.StageInit,
	}
	reporter.Report(event)

	// Test passes if no panic occurs
}

func TestRPCProgressReporter_NotifyError(t *testing.T) {
	// Create a mock notifier that returns an error
	mockNotifier := &mockRPCNotifier{
		notifyError: errors.New("notification failed"),
	}

	// Create RPC progress reporter
	reporter := newRPCProgressReporterForTest(mockNotifier, logr.Discard())

	// Should not panic when Notify returns an error
	event := progress.ProgressEvent{
		Stage: progress.StageInit,
	}
	reporter.Report(event)

	// Verify the notification was attempted
	notifications := mockNotifier.getNotifications()
	if len(notifications) != 1 {
		t.Fatalf("expected 1 notification attempt, got %d", len(notifications))
	}

	// Test passes if no panic occurs despite error
}

func TestMultiProgressReporter_MultipleReporters(t *testing.T) {
	// Create two mock notifiers
	mockNotifier1 := &mockRPCNotifier{}
	mockNotifier2 := &mockRPCNotifier{}

	// Create two RPC reporters
	reporter1 := newRPCProgressReporterForTest(mockNotifier1, logr.Discard())
	reporter2 := newRPCProgressReporterForTest(mockNotifier2, logr.Discard())

	// Create multi-reporter
	multiReporter := NewMultiProgressReporter(reporter1, reporter2)

	// Report an event
	event := progress.ProgressEvent{
		Stage:   progress.StageInit,
		Message: "Test",
	}
	multiReporter.Report(event)

	// Verify both reporters received the event
	notifications1 := mockNotifier1.getNotifications()
	if len(notifications1) != 1 {
		t.Errorf("reporter1: expected 1 notification, got %d", len(notifications1))
	}

	notifications2 := mockNotifier2.getNotifications()
	if len(notifications2) != 1 {
		t.Errorf("reporter2: expected 1 notification, got %d", len(notifications2))
	}
}

func TestMultiProgressReporter_EmptyList(t *testing.T) {
	// Create multi-reporter with no reporters
	multiReporter := NewMultiProgressReporter()

	// Should not panic when reporting
	event := progress.ProgressEvent{
		Stage: progress.StageInit,
	}
	multiReporter.Report(event)

	// Test passes if no panic occurs
}

func TestMultiProgressReporter_NilReporters(t *testing.T) {
	// Create multi-reporter with nil reporters
	multiReporter := NewMultiProgressReporter(nil, nil)

	// Should not panic when reporting
	event := progress.ProgressEvent{
		Stage: progress.StageInit,
	}
	multiReporter.Report(event)

	// Test passes if no panic occurs
}

func TestMultiProgressReporter_SingleReporter(t *testing.T) {
	// Create one reporter
	mockNotifier := &mockRPCNotifier{}
	reporter := newRPCProgressReporterForTest(mockNotifier, logr.Discard())

	// Create multi-reporter with single reporter
	// Should return the reporter directly for efficiency
	multiReporter := NewMultiProgressReporter(reporter)

	// Report an event
	event := progress.ProgressEvent{
		Stage: progress.StageInit,
	}
	multiReporter.Report(event)

	// Verify the event was reported
	notifications := mockNotifier.getNotifications()
	if len(notifications) != 1 {
		t.Errorf("expected 1 notification, got %d", len(notifications))
	}
}

func TestMultiProgressReporter_MixedNilAndValid(t *testing.T) {
	// Create reporter mixed with nil
	mockNotifier := &mockRPCNotifier{}
	reporter := newRPCProgressReporterForTest(mockNotifier, logr.Discard())

	// Create multi-reporter with mix of nil and valid
	multiReporter := NewMultiProgressReporter(nil, reporter, nil)

	// Report an event
	event := progress.ProgressEvent{
		Stage: progress.StageInit,
	}
	multiReporter.Report(event)

	// Verify the event was reported to the valid reporter
	notifications := mockNotifier.getNotifications()
	if len(notifications) != 1 {
		t.Errorf("expected 1 notification, got %d", len(notifications))
	}
}

func TestMultiProgressReporter_ConcurrentReporting(t *testing.T) {
	// Create multiple reporters
	mockNotifier1 := &mockRPCNotifier{}
	mockNotifier2 := &mockRPCNotifier{}

	reporter1 := newRPCProgressReporterForTest(mockNotifier1, logr.Discard())
	reporter2 := newRPCProgressReporterForTest(mockNotifier2, logr.Discard())

	multiReporter := NewMultiProgressReporter(reporter1, reporter2)

	// Report from multiple goroutines
	const numGoroutines = 10
	const eventsPerGoroutine = 5

	var wg sync.WaitGroup
	wg.Add(numGoroutines)

	for i := 0; i < numGoroutines; i++ {
		go func(id int) {
			defer wg.Done()
			for j := 0; j < eventsPerGoroutine; j++ {
				event := progress.ProgressEvent{
					Stage:   progress.StageRuleExecution,
					Current: id*eventsPerGoroutine + j,
					Total:   numGoroutines * eventsPerGoroutine,
				}
				multiReporter.Report(event)
			}
		}(i)
	}

	wg.Wait()

	// Verify all events were reported to both reporters
	expectedCount := numGoroutines * eventsPerGoroutine

	notifications1 := mockNotifier1.getNotifications()
	if len(notifications1) != expectedCount {
		t.Errorf("reporter1: expected %d notifications, got %d", expectedCount, len(notifications1))
	}

	notifications2 := mockNotifier2.getNotifications()
	if len(notifications2) != expectedCount {
		t.Errorf("reporter2: expected %d notifications, got %d", expectedCount, len(notifications2))
	}
}
