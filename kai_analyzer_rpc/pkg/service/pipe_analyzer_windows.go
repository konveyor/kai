//go:build windows

package service

import "github.com/go-logr/logr"

func NewPipeAnalyzer(limitIncidents, limitCodeSnips, contextLines int, pipePath, rules string, l logr.Logger) (Analyzer, error) {
	return nil, nil
}
