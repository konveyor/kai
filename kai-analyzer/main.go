package main

import (
	"flag"
	"fmt"
	"log/slog"
	"net/rpc"
	"os"

	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	"github.com/konveyor/kai-analyzer/pkg/service"
)

func main() {

	sourceDirectory := flag.String("source-directory", ".", "This will be the absolute path to the source code directory that should be analyzed")
	rulesDirectory := flag.String("rules-directory", ".", "This will be the absolute path to the rules directory")
	lspServerPath := flag.String("lspServerPath", "/Users/shurley/repos/kai/jdtls/bin/jdtls", "this will be the path to the lsp")
	bundles := flag.String("bundles", "/Users/shurley/repos/MTA/java-analyzer-bundle/java-analyzer-bundle.core/target/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar", "this is the path to the java analyzer bundle")

	flag.Parse()
	// In the future add cobra for flags maybe
	// create log file in working directory for now.

	if sourceDirectory == nil || *sourceDirectory == "" {
		panic(fmt.Errorf("source directory must be valid"))
	}

	if rulesDirectory == nil || *rulesDirectory == "" {
		panic(fmt.Errorf("rules directory must be valid"))
	}

	logger := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{
		Level: slog.Level(-100),
	})

	l := logr.FromSlogHandler(logger)
	l.Info("Starting Analyzer", "source-dir", *sourceDirectory, "rules-dir", *rulesDirectory)
	// We need to start up the JSON RPC server and start listening for messages
	analyzerService, err := service.NewAnalyzer(
		10000, 10, 10,
		*sourceDirectory,
		"",
		*lspServerPath,
		*bundles,
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
	server.ServeRequest(codec)
}
