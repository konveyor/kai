package codec

import "encoding/json"

// serverRequest and clientResponse combined
type message struct {
	Method         string           `json:"method"`
	Params         *json.RawMessage `json:"params"`
	Id             *json.RawMessage `json:"id,omitempty"`
	Result         *json.RawMessage `json:"result"`
	Error          interface{}      `json:"error"`
	JsonRPCVersion string           `json:"jsonrpc"`
}

// Unmarshal to
type serverRequest struct {
	Method         string           `json:"method"`
	Params         *json.RawMessage `json:"params"`
	Id             *json.RawMessage `json:"id"`
	unMarshalledId *uint64          `json:"-"`
}
type clientResponse struct {
	Id             uint64           `json:"id"`
	Result         *json.RawMessage `json:"result"`
	Error          interface{}      `json:"error"`
	JsonRPCVersion string           `json:"jsonrpc"`
}

// to Marshal
type serverResponse struct {
	Id             *json.RawMessage `json:"id"`
	Result         interface{}      `json:"result"`
	Error          interface{}      `json:"error"`
	JsonRPCVersion string           `json:"jsonrpc"`
}
type clientRequest struct {
	Method         string      `json:"method"`
	Params         interface{} `json:"params"`
	Id             *uint64     `json:"id"`
	JsonRPCVersion string      `json:"jsonrpc"`
}
