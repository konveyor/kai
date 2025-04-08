package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"io"
	"log/slog"
	"net/rpc"
	"os"
	"os/exec"
	"os/signal"
	"syscall"

	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	klog "github.com/konveyor/kai-analyzer/pkg/log"
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
	inputLogLevel := flag.String("log-level", "DEBUG-1", "Log level")

	flag.Parse()

	var logLevel slog.Level
	err := logLevel.UnmarshalText([]byte(*inputLogLevel))
	if err != nil {
		panic(fmt.Errorf("invalid log level"))
	}

	if sourceDirectory == nil || *sourceDirectory == "" {
		panic(fmt.Errorf("source directory must be valid"))
	}

	if rules == nil || *rules == "" {
		panic(fmt.Errorf("rules must be set"))
	}

	if lspServerPath == nil || *lspServerPath == "" {
		panic(fmt.Errorf("lspServerPath must be set"))
	}

	if bundles == nil || *bundles == "" {
		panic(fmt.Errorf("bundles must be set"))
	}

	// fileLogger is for user facing logs that contains
	// detailed analysis logs
	fileLogger := slog.NewJSONHandler(io.Discard, nil)
	if logFile != nil && *logFile != "" {
		file, err := os.Create(*logFile)
		if err != nil {
			panic(err)
		}
		fileLogger = slog.NewJSONHandler(file, &slog.HandlerOptions{
			Level: logLevel,
		})
	}

	// stderrLogger is for internal logs discovered by the extension
	stderrLogger := slog.NewTextHandler(os.Stderr, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	})

	l := logr.FromSlogHandler(klog.NewCombinedHandler(stderrLogger, fileLogger))

	l.Info("using logLevel", "logLevel", logLevel)

	// Check if Java exists on the PATH
	if err := exec.Command("java", "-version").Run(); err != nil {
		panic("Java is not installed or not on the PATH")
	}
	l.Info("Java is installed")

	// Check if Maven exists on the PATH
	if err := exec.Command("mvn", "-version").Run(); err != nil {
		panic("Maven is not installed or not on the PATH")
	}
	l.Info("Maven is installed")

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
	server := rpc.NewServer()
	err = server.RegisterName("analysis_engine", analyzerService)
	if err != nil {
		panic(err)
	}

	cancelChan := make(chan os.Signal, 1)
	// catch SIGETRM or SIGINTERRUPT
	signal.Notify(cancelChan, syscall.SIGTERM, syscall.SIGINT)
	codec := codec.NewCodec(codec.Connection{Input: os.Stdin, Output: os.Stdout}, l)
	go func() {
		l.Info("Starting Server")
		server.ServeCodec(codec)
	}()

	sig := <-cancelChan
	// When we get here, call stop on the analyzer server
	l.Info("stopping server", "signal", sig)
	analyzerService.Stop()
}
