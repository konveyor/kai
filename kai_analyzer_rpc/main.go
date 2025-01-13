package main

import (
	"flag"
	"fmt"
	"log/slog"
	"net/rpc"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"syscall"

	"github.com/go-logr/logr"
	"github.com/konveyor/kai-analyzer/pkg/codec"
	"github.com/konveyor/kai-analyzer/pkg/service"
)

type arrayVar []string

func (i *arrayVar) String() string {
	if i == nil {
		return ""
	}
	return strings.Join(*i, ",")
}

func (i *arrayVar) Set(value string) error {
	*i = append(*i, value)
	return nil
}

var rulesDirectories arrayVar

func main() {

	sourceDirectory := flag.String("source-directory", ".", "This will be the absolute path to the source code directory that should be analyzed")
	flag.Var(&rulesDirectories, "rules", "Path to rules directory. Use multiple times for additional rules: --rules <rule1> --rules <rule2> ...")
	logFile := flag.String("log-file", "", "This is the file where logs should be stored. By default they will just be written to stderr")
	lspServerPath := flag.String("lspServerPath", "/Users/shurley/repos/kai/jdtls/bin/jdtls", "this will be the path to the lsp")
	bundles := flag.String("bundles", "/Users/shurley/repos/MTA/java-analyzer-bundle/java-analyzer-bundle.core/target/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar", "this is the path to the java analyzer bundle")
	depOpenSourceLabelsFile := flag.String("depOpenSourceLabelsFile", "", "Path to the dep open source labels file")

	// TODO(djzager): We should do verbosity type argument(s)
	logLevel := slog.LevelDebug

	flag.Parse()
	// In the future add cobra for flags maybe
	// create log file in working directory for now.

	if sourceDirectory == nil || *sourceDirectory == "" {
		panic(fmt.Errorf("source directory must be valid"))
	}

	if rulesDirectories == nil || (len(rulesDirectories) == 0) {
		panic(fmt.Errorf("rules directories must be valid"))
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

	l.Info("Starting Analyzer", "source-directory", *sourceDirectory, "rules-directories", rulesDirectories, "lspServerPath", *lspServerPath, "bundles", *bundles, "depOpenSourceLabelsFile", *depOpenSourceLabelsFile)
	// We need to start up the JSON RPC server and start listening for messages
	analyzerService, err := service.NewAnalyzer(
		10000, 10, 10,
		*sourceDirectory,
		"",
		*lspServerPath,
		*bundles,
		*depOpenSourceLabelsFile,
		rulesDirectories,
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
