package log

import (
	"context"
	"errors"
	"log/slog"
)

type compositeHandler struct {
	handlers []slog.Handler
}

func (c *compositeHandler) Enabled(ctx context.Context, lvl slog.Level) bool {
	for _, h := range c.handlers {
		if h.Enabled(ctx, lvl) {
			return true
		}
	}
	return false
}

func (c *compositeHandler) Handle(ctx context.Context, record slog.Record) error {
	errs := []error{}
	for _, h := range c.handlers {
		if h.Enabled(ctx, record.Level) {
			if err := h.Handle(ctx, record); err != nil {
				errs = append(errs, err)
			}
		}
	}
	if len(errs) > 0 {
		return errors.Join(errs...)
	}
	return nil
}

func (c *compositeHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	handlers := []slog.Handler{}
	for _, h := range c.handlers {
		handlers = append(handlers, h.WithAttrs(attrs))
	}
	return &compositeHandler{handlers: handlers}
}

func (c *compositeHandler) WithGroup(name string) slog.Handler {
	handlers := []slog.Handler{}
	for _, h := range c.handlers {
		handlers = append(handlers, h.WithGroup(name))
	}
	return &compositeHandler{handlers: handlers}
}

func NewCombinedHandler(hs ...slog.Handler) slog.Handler {
	return &compositeHandler{
		handlers: hs,
	}
}
