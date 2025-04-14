package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"log/slog"
	"os"
	"os/exec"
	"os/signal"
	"syscall"

	rpc "github.com/cenkalti/rpc2"

	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	kairpc "github.com/konveyor/kai-analyzer/pkg/rpc"
	"github.com/konveyor/kai-analyzer/pkg/service"
	"github.com/konveyor/kai-analyzer/pkg/tracing"
)

func main() {
	sourceDirectory := flag.String("source-directory", ".", "This will be the absolute path to the source code directory that should be analyzed")
	rules := flag.String("rules", "", "Comma separated list of absolute path to rules directories")
	logFile := flag.String("log-file", "", "This is the file where logs should be stored. By default they will just be written to stderr")
	lspServerPath := flag.String("lspServerPath", "", "this will be the path to the lsp")
	bundles := flag.String("bundles", "", "Comma separated list of path to java analyzer bundles")
	depOpenSourceLabelsFile := flag.String("depOpenSourceLabelsFile", "", "Path to the dep open source labels file")
	pipePath := flag.String("pipePath", "", "Path to the pipe to use for bi-directional communication")
	logVerbosity := flag.Int("verbosity", -4, "how verbose would you like the logs to be, error logs are 8, warning logs are 4 info logs are 0 and debug logs are -4, going more negative gives more logs.")

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
	usingPipe, err := validateFlags(sourceDirectory, rules, lspServerPath, bundles, depOpenSourceLabelsFile, pipePath, l)
	if err != nil {
		panic(err)
	}

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
	// catch SIGETRM or SIGINTERRUPT
	signal.Notify(cancelChan, syscall.SIGTERM, syscall.SIGINT)
	//serverCodec := codec.NewCodec(codec.Connection{Input: os.Stdin, Output: os.Stdout, Logger: l}, l)
	go func() {
		l.Info("Starting Server")
		var s *kairpc.Server
		if !usingPipe {
			l.Info("Starting Analyzer", "source-dir", *sourceDirectory, "rules-dir", *rules, "lspServerPath", *lspServerPath, "bundles", *bundles, "depOpenSourceLabelsFile", *depOpenSourceLabelsFile)
			// We need to start up the JSON RPC server and start listening for messages
			analyzerService, err := service.NewAnalyzer(
				10000, 10, 10,
				*sourceDirectory,
				"",
				*lspServerPath,
				*bundles,
				*depOpenSourceLabelsFile,
				*rules,
				l,
			)
			if err != nil {
				panic(err)
			}
			server.Handle("analysis_engine.Analyze", analyzerService.Analyze)
			codec := codec.NewConnectionCodec(codec.Connection{Input: os.Stdin, Output: os.Stdout}, l)
			server.ServeCodec(codec)
		} else {
			s = kairpc.NewServer(ctx, server, l, "notification.Notify", *rules, *sourceDirectory)
			s.Accept(*pipePath)
		}
		l.Info("Stopping Server")
	}()

	sig := <-cancelChan
	cancelFunc()
	// When we get here, call stop on the analyzer server
	l.Info("stopping server", "signal", sig)

}

func validateFlags(sourceDirectory, rules, lspServerPath, bundles, depOpenSourceLabelsFile, pipePath *string, l logr.Logger) (bool, error) {
	// If we are using a named pipe, jdtls is initialized by the caller.
	if pipePath != nil && *pipePath != "" && rules != nil && len(*rules) > 0 && sourceDirectory != nil && *sourceDirectory != "" {
		return true, nil
	}

	if sourceDirectory == nil || *sourceDirectory == "" {
		return false, fmt.Errorf("source directory must be valid")
	}

	if rules == nil || *rules == "" {
		return false, fmt.Errorf("rules must be set")
	}

	if lspServerPath == nil || *lspServerPath == "" {
		return false, fmt.Errorf("lspServerPath must be set")
	}

	if bundles == nil || *bundles == "" {
		return false, fmt.Errorf("bundles must be set")
	}
	// Check if Java exists on the PATH
	if err := exec.Command("java", "-version").Run(); err != nil {
		return false, fmt.Errorf("java is not installed or not on the PATH")
	}
	l.Info("Java is installed")

	// Check if Maven exists on the PATH
	if err := exec.Command("mvn", "-version").Run(); err != nil {
		return false, fmt.Errorf("maven is not installed or not on the PATH")
	}
	l.Info("Maven is installed")
	return false, nil

}
