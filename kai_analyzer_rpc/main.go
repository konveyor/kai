package main

import (
	"flag"
	"fmt"
	"log/slog"
	"net/rpc"
	"os"
	"os/exec"

	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	"github.com/konveyor/kai-analyzer/pkg/service"
)

func main() {

	sourceDirectory := flag.String("source-directory", ".", "This will be the absolute path to the source code directory that should be analyzed")
	rulesDirectory := flag.String("rules-directory", ".", "This will be the absolute path to the rules directory")
	logFile := flag.String("log-file", "", "This is the file where logs should be stored. By default they will just be written to stderr")
	lspServerPath := flag.String("lspServerPath", "/Users/shurley/repos/kai/jdtls/bin/jdtls", "this will be the path to the lsp")
	bundles := flag.String("bundles", "/Users/shurley/repos/MTA/java-analyzer-bundle/java-analyzer-bundle.core/target/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar", "this is the path to the java analyzer bundle")
	depOpenSourceLabelsFile := flag.String("depOpenSourceLabelsFile", "", "Path to the dep open source labels file")

	// TODO(djzager): We should do verbosity type argument(s)
	logLevel := slog.LevelInfo

	flag.Parse()
	// In the future add cobra for flags maybe
	// create log file in working directory for now.

	if sourceDirectory == nil || *sourceDirectory == "" {
		panic(fmt.Errorf("source directory must be valid"))
	}

	if rulesDirectory == nil || *rulesDirectory == "" {
		panic(fmt.Errorf("rules directory must be valid"))
	}

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

	l.Info("Starting Analyzer", "source-dir", *sourceDirectory, "rules-dir", *rulesDirectory, "lspServerPath", *lspServerPath, "bundles", *bundles, "depOpenSourceLabelsFile", *depOpenSourceLabelsFile)
	// We need to start up the JSON RPC server and start listening for messages
	analyzerService, err := service.NewAnalyzer(
		10000, 10, 10,
		*sourceDirectory,
		"",
		*lspServerPath,
		*bundles,
		*depOpenSourceLabelsFile,
		[]string{*rulesDirectory},
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

	codec := codec.NewCodec(codec.Connection{Input: os.Stdin, Output: os.Stdout}, l)
	l.Info("Starting Server")
	server.ServeCodec(codec)
}
