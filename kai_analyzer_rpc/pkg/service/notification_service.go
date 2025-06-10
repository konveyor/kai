package service

import (
	rpc "github.com/cenkalti/rpc2"
	"github.com/go-logr/logr"
)

type NotificationService struct {
	Logger logr.Logger
}

func (n *NotificationService) Notify(client *rpc.Client, args map[string]interface{}, response *Response) error {
	n.Logger.Info("here in notification service !! Notify", "args", args)
	if v, ok := args["type"]; ok {
		if v == "start" {
			err := client.Notify("started", nil)
			if err != nil {
				n.Logger.Error(err, "could not notify")
			}
		}

	}
	return nil
}
