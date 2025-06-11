package client

import (
	"context"

	"github.com/cenkalti/rpc2"
)

type Client struct {
	*rpc2.Client
}

func (c *Client) Call(ctx context.Context, method string, args interface{}, reply interface{}) error {
	return c.Client.CallWithContext(ctx, method, args, reply)
}

func (c *Client) Notify(ctx context.Context, method string, args interface{}) error {
	return c.Client.Notify(method, args)
}
