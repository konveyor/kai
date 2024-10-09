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

	flag.Parse()
	// In the future add cobra for flags maybe
	// create log file in working directory for now.

	if sourceDirectory == nil || *sourceDirectory == "" {
		panic(fmt.Errorf("source directory must be valid"))
	}

	if rulesDirectory == nil || *rulesDirectory == "" {
		panic(fmt.Errorf("rules directory must be valid"))
	}

	file, err := os.Create("kai-analyzer.log")
	if err != nil {
		panic(err)
	}
	logger := slog.NewJSONHandler(file, &slog.HandlerOptions{
		Level: slog.Level(-100),
	})

	l := logr.FromSlogHandler(logger)
	l.Info("Starting Analyzer", "source-dir", *sourceDirectory, "rules-dir", *rulesDirectory)
	// We need to start up the JSON RPC server and start listening for messages
	analyzerService, err := service.NewAnalyzer(10000, 10, 10, *sourceDirectory, "", []string{*rulesDirectory}, l)
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
	err = server.ServeRequest(codec)
	// If we can not start the server it is reasonable to panic and get the full error info
	if err != nil {
		panic(err)
	}
}
