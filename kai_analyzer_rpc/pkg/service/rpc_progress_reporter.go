package service

import (
	rpc "github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
)

// RPCNotifier is an interface for sending RPC notifications.
// This interface allows for easier testing by enabling mock implementations.
type RPCNotifier interface {
	Notify(method string, args interface{}) error
}

// RPCProgressReporter sends progress notifications through the RPC channel.
//
// This reporter implements progress.ProgressReporter by sending events
// as RPC notifications to the "analysis.progress" method. This allows
// clients to receive real-time progress updates through the established
// RPC channel without parsing stderr/stdout streams.
//
// Progress events include all stages of analysis:
//   - StageInit: Analyzer initialization begins
//   - StageProviderInit: Provider initialization (per provider, with messages)
//   - StageRuleParsing: Rules loaded (includes total count)
//   - StageRuleExecution: Per-rule progress (includes current, total, percent)
//   - StageComplete: Analysis finished
//
// The reporter is safe for concurrent use and handles errors internally
// by logging them without disrupting the analysis process.
type RPCProgressReporter struct {
	notifier RPCNotifier
	logger   logr.Logger
}

// NewRPCProgressReporter creates a new RPC-based progress reporter.
//
// Parameters:
//   - client: The RPC client to send notifications through
//   - logger: Logger for error handling and debugging
//
// Returns a ProgressReporter that sends events via RPC notifications.
func NewRPCProgressReporter(client *rpc.Client, logger logr.Logger) progress.ProgressReporter {
	return &RPCProgressReporter{
		notifier: client,
		logger:   logger,
	}
}

// Report sends a progress event as an RPC notification.
//
// This method implements progress.ProgressReporter.Report() by sending
// the event to the "analysis.progress" notification endpoint. Errors
// are logged but do not disrupt the analysis process.
//
// The method is safe for concurrent use and does not block, as
// rpc.Client.Notify() is non-blocking.
func (r *RPCProgressReporter) Report(event progress.ProgressEvent) {
	if r.notifier == nil {
		r.logger.V(5).Info("RPC notifier is nil, skipping progress notification")
		return
	}

	err := r.notifier.Notify("analysis.progress", event)
	if err != nil {
		r.logger.Error(err, "failed to send progress notification",
			"stage", event.Stage,
			"message", event.Message,
			"current", event.Current,
			"total", event.Total,
		)
	} else {
		r.logger.V(5).Info("sent progress notification",
			"stage", event.Stage,
			"message", event.Message,
			"percent", event.Percent,
		)
	}
}
