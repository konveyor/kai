package service

import (
	"github.com/konveyor/analyzer-lsp/progress"
)

// MultiProgressReporter sends progress events to multiple reporters.
//
// This reporter allows progress events to be sent to multiple destinations
// simultaneously, enabling both RPC-based and stream-based progress reporting
// to work together for backward compatibility.
//
// The reporter is safe for concurrent use as it delegates to the underlying
// reporters, which are required to be thread-safe.
type MultiProgressReporter struct {
	reporters []progress.ProgressReporter
}

// NewMultiProgressReporter creates a progress reporter that sends to multiple destinations.
//
// Parameters:
//   - reporters: List of reporters to send events to
//
// Returns a ProgressReporter that forwards events to all provided reporters.
// If the list is empty, returns a noop reporter. If there's only one reporter,
// returns that reporter directly for efficiency.
func NewMultiProgressReporter(reporters ...progress.ProgressReporter) progress.ProgressReporter {
	// Filter out nil reporters
	validReporters := make([]progress.ProgressReporter, 0, len(reporters))
	for _, r := range reporters {
		if r != nil {
			validReporters = append(validReporters, r)
		}
	}

	// Optimize for common cases
	switch len(validReporters) {
	case 0:
		return progress.NewNoopReporter()
	case 1:
		return validReporters[0]
	default:
		return &MultiProgressReporter{reporters: validReporters}
	}
}

// Report sends the progress event to all configured reporters.
//
// This method implements progress.ProgressReporter.Report() by forwarding
// the event to each underlying reporter. If a reporter fails, the error
// is handled internally by that reporter and does not affect other reporters.
//
// The method is safe for concurrent use.
func (m *MultiProgressReporter) Report(event progress.ProgressEvent) {
	for _, reporter := range m.reporters {
		reporter.Report(event)
	}
}
