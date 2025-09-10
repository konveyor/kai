package service

import (
	"path/filepath"
	"strings"

	"github.com/go-logr/logr"
	"github.com/konveyor/analyzer-lsp/output/v1/konveyor"
)

type IncidentsCache interface {
	Get(path string) ([]CacheValue, bool)
	Add(path string, value CacheValue)
	Delete(path string)
	Len() int
	Entries() map[string][]CacheValue
}

type CacheValue struct {
	Incident      konveyor.Incident
	ViolationName string
	Violation     konveyor.Violation
	Ruleset       konveyor.RuleSet
}

func NewIncidentsCache(logger logr.Logger) IncidentsCache {
	return &incidentsCache{
		cache:  map[string][]CacheValue{},
		logger: logger,
	}
}

type incidentsCache struct {
	cache  map[string][]CacheValue
	logger logr.Logger
}

func (i *incidentsCache) Len() int {
	return len(i.cache)
}

func (i *incidentsCache) Get(path string) ([]CacheValue, bool) {
	normalizedPath := normalizePath(path)
	i.logger.V(8).Info("getting cache entry for path", "path", path, "normalizedPath", normalizedPath)
	val, ok := i.cache[normalizedPath]
	return val, ok
}

func (i *incidentsCache) Add(path string, value CacheValue) {
	normalizedPath := normalizePath(path)
	i.logger.V(8).Info("adding cache entry for path", "path", path, "normalizedPath", normalizedPath)
	if _, ok := i.cache[normalizedPath]; !ok {
		i.cache[normalizedPath] = []CacheValue{}
	}
	i.cache[normalizedPath] = append(i.cache[normalizedPath], value)
}

func (i *incidentsCache) Delete(path string) {
	normalizedPath := normalizePath(path)
	i.logger.V(8).Info("deleting cache entry for path", "path", path, "normalizedPath", normalizedPath)
	delete(i.cache, normalizedPath)
}

func (i *incidentsCache) Keys() []string {
	keys := make([]string, 0, len(i.cache))
	for k := range i.cache {
		keys = append(keys, k)
	}
	return keys
}

func (i *incidentsCache) Entries() map[string][]CacheValue {
	return i.cache
}

func normalizePath(path string) string {
	cleanedPath := filepath.Clean(path)
	volumeName := filepath.VolumeName(cleanedPath)
	// make sure all volume names are lowercase
	if volumeName != "" {
		cleanedPath = strings.ToUpper(volumeName) + cleanedPath[len(volumeName):]
	}
	return filepath.ToSlash(cleanedPath) // prevent forward / backward slashes becoming a problem
}
