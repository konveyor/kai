package main

import (
	"context"
	"errors"
	"flag"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	rpc "github.com/cenkalti/rpc2"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
	kairpc "github.com/konveyor/kai-analyzer/pkg/rpc"
	"github.com/konveyor/kai-analyzer/pkg/service"
	"github.com/konveyor/kai-analyzer/pkg/tracing"
)

func main() {
	rules := flag.String("rules", "", "Comma separated list of absolute path to rules directories")
	logFile := flag.String("log-file", "", "This is the file where logs should be stored. By default they will just be written to stderr")
	serverPipe := flag.String("server-pipe", "", "Path to the pipe to use for bi-directional communication")
	providerConfigFile := flag.String("provider-config", "", "Path the provider config file")
	logVerbosity := flag.Int("verbosity", -4, "how verbose would you like the logs to be, error logs are 8, warning logs are 4 info logs are 0 and debug logs are -4, going more negative gives more logs.")
	progressOutput := flag.String("progress-output", "", "Where to write progress events (stderr, stdout, or file path)")
	progressFormat := flag.String("progress-format", "json", "Format for progress output: text or json")

	// TODO(djzager): We should do verbosity type argument(s)
	logLevel := slog.Level(*logVerbosity)

	flag.Parse()
	// In the future add cobra for flags maybe
	// create log file in working directory for now.

	// TODO(djzager): Handle log level/location more like reputable LSP servers
	// ChatGPT told me gopls and jdtls default to stderr but I couldn't confirm that
	// for now I think it's enough to make it configurable to be one or the other.
	// The editor extension(s) can tee stderr to a temp file.
	var logger *slog.JSONHandler
	if logFile != nil && *logFile != "" {
		file, err := os.Create(*logFile)
		if err != nil {
			panic(err)
		}
		logger = slog.NewJSONHandler(file, &slog.HandlerOptions{
			Level: slog.Level(logLevel),
		})
	} else {
		logger = slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{
			Level: slog.Level(logLevel),
		})
	}

	l := logr.FromSlogHandler(logger)

	l.Info("args", "rules", rules, "logFile", logFile, "serverPipe", serverPipe, "providerConfig", providerConfigFile, "verbosity", logVerbosity, "progressOutput", progressOutput, "progressFormat", progressFormat)

	// Create progress reporter
	progressReporter, cleanupProgress := createProgressReporter(*progressOutput, *progressFormat, l)
	defer cleanupProgress()

	// Check if ENABLE_TRACING is set in the environment.
	if _, enable_tracing := os.LookupEnv("ENABLE_TRACING"); enable_tracing {
		// Set up OpenTelemetry.
		otelShutdown, err := tracing.SetupOTelSDK(context.Background())
		if err != nil {
			return
		}

		// Handle shutdown properly so nothing leaks.
		defer func() {
			err = errors.Join(err, otelShutdown(context.Background()))
		}()
	}
	server := rpc.NewServer()
	notificationService := &service.NotificationService{Logger: l}
	server.Handle("notification.Notify", notificationService.Notify)

	ctx, cancelFunc := context.WithCancel(context.Background())
	cancelChan := make(chan os.Signal, 1)
	// catch SIGTERM or SIGINT
	signal.Notify(cancelChan, syscall.SIGTERM, syscall.SIGINT)
	go func() {
		l.Info("Starting Server")
		s := kairpc.NewServer(ctx, server, l, "notification.Notify", *rules, *providerConfigFile, progressReporter)
		s.OnConnect(func(c *rpc.Client) {
			err := c.Notify("started", nil)
			if err != nil {
				l.Error(err, "Failed to send server started notification")
			} else {
				l.Info("Successfully sent server started notification")
			}
		})
		s.Accept(*serverPipe)
		l.Info("Stopping Server")
	}()

	sig := <-cancelChan
	cancelFunc()
	// When we get here, call stop on the analyzer server
	l.Info("stopping server", "signal", sig)

}

// createProgressReporter creates the appropriate progress reporter based on CLI flags.
//
// The progressOutput parameter specifies where to write progress events:
//   - "" (empty): Returns NoopReporter with zero overhead
//   - "stderr": Writes to standard error
//   - "stdout": Writes to standard output
//   - any other value: Treats as file path and creates the file
//
// The progressFormat parameter specifies the output format:
//   - "json": NDJSON format for programmatic consumption
//   - "text": Human-readable format
//   - any other value: Defaults to JSON format
//
// Returns a ProgressReporter and a cleanup function. The cleanup function
// must be called (typically via defer) to properly close any opened files.
//
// If file creation fails, the function logs a warning and falls back to stderr.
//
// Example usage:
//
//	reporter, cleanup := createProgressReporter("stderr", "json", logger)
//	defer cleanup()
func createProgressReporter(progressOutput, progressFormat string, l logr.Logger) (progress.ProgressReporter, func()) {
	// If no progress output specified, use noop reporter (zero overhead)
	if progressOutput == "" {
		return progress.NewNoopReporter(), func() {}
	}

	var writer *os.File
	cleanup := func() {}

	switch progressOutput {
	case "stderr":
		writer = os.Stderr
	case "stdout":
		writer = os.Stdout
	default:
		// Try to create a file
		file, err := os.Create(progressOutput)
		if err != nil {
			l.Error(err, "failed to create progress output file, falling back to stderr", "path", progressOutput)
			writer = os.Stderr
		} else {
			writer = file
			cleanup = func() { file.Close() }
		}
	}

	// Create the appropriate reporter based on format
	var reporter progress.ProgressReporter
	switch progressFormat {
	case "json":
		reporter = progress.NewJSONReporter(writer)
	case "text":
		reporter = progress.NewTextReporter(writer)
	default:
		l.Info("unknown progress format, defaulting to json", "format", progressFormat)
		reporter = progress.NewJSONReporter(writer)
	}

	l.Info("progress reporting enabled", "output", progressOutput, "format", progressFormat)
	return reporter, cleanup
}
