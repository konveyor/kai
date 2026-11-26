package main

import (
	"context"
	"flag"
	"fmt"
	"log/slog"
	"os"
	"os/signal"
	"runtime/debug"
	"syscall"

	rpc "github.com/cenkalti/rpc2"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/progress"
	progressreporter "github.com/konveyor/analyzer-lsp/progress/reporter"
	kairpc "github.com/konveyor/kai-analyzer/pkg/rpc"
	"github.com/konveyor/kai-analyzer/pkg/service"
	"github.com/konveyor/kai-analyzer/pkg/tracing"
)

// version and commit are set at build time, for example:
//
//	go build -ldflags "-X main.version=v0.9.0 -X main.commit=$(git rev-parse HEAD)"
//
// When commit is not set the VCS revision recorded by the Go toolchain is
// used instead, which is only available for builds that do not name main.go
// on the command line.
var (
	version = "dev"
	commit  = ""
)

func main() {
	showVersion := flag.Bool("version", false, "Print the version and commit of this binary and exit")
	rules := flag.String("rules", "", "Comma separated list of absolute path to rules directories")
	logFile := flag.String("log-file", "", "This is the file where logs should be stored. By default they will just be written to stderr")
	serverPipe := flag.String("server-pipe", "", "Path to the pipe to use for bi-directional communication")
	providerConfigFile := flag.String("provider-config", "", "Path the provider config file")
	logVerbosity := flag.Int("verbosity", -4, "how verbose would you like the logs to be, error logs are 8, warning logs are 4 info logs are 0 and debug logs are -4, going more negative gives more logs.")
	progressOutput := flag.String("progress-output", "", "Where to write progress events (stderr, stdout, or file path)")
	progressFormat := flag.String("progress-format", "json", "Format for progress output: text or json")

	flag.Parse()

	if *showVersion {
		fmt.Println(versionString())
		return
	}

	// TODO(djzager): We should do verbosity type argument(s)
	// In the future add cobra for flags maybe
	// create log file in working directory for now.

	// TODO(djzager): Handle log level/location more like reputable LSP servers
	// ChatGPT told me gopls and jdtls default to stderr but I couldn't confirm that
	// for now I think it's enough to make it configurable to be one or the other.
	// The editor extension(s) can tee stderr to a temp file.
	logger, closeLog, err := newLogHandler(*logFile, *logVerbosity)
	if err != nil {
		fmt.Fprintf(os.Stderr, "unable to create log file: %v\n", err)
		os.Exit(1)
	}
	defer closeLog()

	l := logr.FromSlogHandler(logger)

	l.Info("starting", "version", version, "commit", resolvedCommit())
	l.Info("args", "rules", rules, "logFile", logFile, "serverPipe", serverPipe, "providerConfig", providerConfigFile, "verbosity", logVerbosity, "progressOutput", progressOutput, "progressFormat", progressFormat)

	// Create progress reporter for stream-based output (stderr/stdout/file).
	// Note: During analysis, progress events are also sent via RPC notifications
	// to the "analysis.progress" method for real-time client updates.
	progressReporter, cleanupProgress := createProgressReporter(*progressOutput, *progressFormat, l)
	defer cleanupProgress()

	// Check if ENABLE_TRACING is set in the environment.
	if _, enable_tracing := os.LookupEnv("ENABLE_TRACING"); enable_tracing {
		// Set up OpenTelemetry.
		otelShutdown, err := tracing.SetupOTelSDK(context.Background())
		if err != nil {
			// Tracing is optional, so a failure here should not take the
			// analyzer down without a word.
			l.Error(err, "unable to set up tracing, continuing without it")
		} else {
			// Handle shutdown properly so nothing leaks.
			defer func() {
				if err := otelShutdown(context.Background()); err != nil {
					l.Error(err, "unable to shut down tracing")
				}
			}()
		}
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
// This creates a stream-based reporter for writing progress to stderr/stdout/file.
// During analysis, progress events are ALSO sent via RPC notifications to the
// "analysis.progress" method, allowing clients to receive real-time updates through
// the RPC channel without parsing streams.
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
func createProgressReporter(progressOutput, progressFormat string, l logr.Logger) (progress.Reporter, func()) {
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
	var reporter progress.Reporter
	switch progressFormat {
	case "json":
		reporter = progressreporter.NewJSONReporter(writer)
	case "text":
		reporter = progressreporter.NewTextReporter(writer)
	default:
		l.Info("unknown progress format, defaulting to json", "format", progressFormat)
		reporter = progressreporter.NewJSONReporter(writer)
	}

	l.Info("progress reporting enabled", "output", progressOutput, "format", progressFormat)
	return reporter, cleanup
}

// newLogHandler builds the JSON log handler for the given log file and
// verbosity. An empty logFile means stderr. The returned function closes the
// log file, if one was opened.
func newLogHandler(logFile string, verbosity int) (*slog.JSONHandler, func(), error) {
	opts := &slog.HandlerOptions{Level: slog.Level(verbosity)}
	if logFile == "" {
		return slog.NewJSONHandler(os.Stderr, opts), func() {}, nil
	}
	file, err := os.Create(logFile)
	if err != nil {
		return nil, nil, err
	}
	return slog.NewJSONHandler(file, opts), func() { file.Close() }, nil
}

// resolvedCommit returns the commit injected at build time, falling back to
// the VCS revision stamped by the Go toolchain.
func resolvedCommit() string {
	if commit != "" {
		return commit
	}
	info, ok := debug.ReadBuildInfo()
	if !ok {
		return "unknown"
	}
	rev, modified := "", false
	for _, setting := range info.Settings {
		switch setting.Key {
		case "vcs.revision":
			rev = setting.Value
		case "vcs.modified":
			modified = setting.Value == "true"
		}
	}
	if rev == "" {
		return "unknown"
	}
	if modified {
		rev += "-dirty"
	}
	return rev
}

func versionString() string {
	return fmt.Sprintf("version: %s\ncommit: %s", version, resolvedCommit())
}
