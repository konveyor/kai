- [Proxy Support](#proxy-support)
  - [Objective](#objective)
  - [Considerations](#considerations)
  - [Common Proxy Coordinate Examples](#common-proxy-coordinate-examples)
  - [Common Self-signed Cert and Validation Examples](#common-self-signed-cert-and-validation-examples)
  - [Additional Configuration Examples](#additional-configuration-examples)
  - [Testing Proxy Support](#testing-proxy-support)

# Proxy Support

## Objective

The aim of our implementation is to support as many use cases as possible by implementing a flexible design.

## Considerations
- Kai is written in python and most python libraries allow for proxy configuration by use of environment variables.
- These include environment variables for specifying a proxy endpoint as well as handling self-signed certificates.
- Some of these environment variables are well known to us and others such as `HTTP_PROXY`, but other less common options may be relevant in some environments
- We should aim for a design that allows for the passing of arbitary environment variable key/value pairs to support the maximum number of cases.

## Common Proxy Coordinate Examples
Python requests honors `HTTP_PROXY` and `HTTPS_PROXY` environment variables for making connections. [[1](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)]

In addition langchains ChatOpenAI relies on setting `OPENAI_PROXY`. [[2](https://github.com/langchain-ai/langchain/discussions/22591)]

An example of setting these to use a proxy running on port 8080 on localhost might look like:

```
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080
export OPENAI_PROXY=http://localhost:8080
```

## Common Self-signed Cert and Validation Examples
In order to make connections to proxies or services with self-signed certificates additional environment variables must be set to load the proxy certificate and disable HTTPS verification.

A generic example may look like
```
export REQUESTS_CA_BUNDLE=~/.mitmproxy/mitmproxy-ca-cert.pem
export SSL_CERT_FILE=~/.mitmproxy/mitmproxy-ca-cert.pem
export PYTHONHTTPSVERIFY=0
```

## Additional Configuration Examples
Some environment variables may be relevant to only some environments include `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET`, which are commonly used in OAUTH2 authorization workflows

In addition `ALL_PROXY` and `NO_PROXY` may also be required for some environments. A scenario may include using a proxy for external providers, while allowing direct access to internal models.

## Testing Proxy Support
[mitmproxy](https://github.com/mitmproxy/mitmproxy) is a powerful proxy geared towards development and penetration testing. At the same time it is easy to configure and view connection details from with the TUI.

On Linux it will create certificates on the first run that allow for testing functionality with self-signed proxy certificates. The CA cert can be found at `~/.mitmproxy/mitmproxy-ca-cert.pem`.

The proxy can be invoken as simply as `mitmproxy -p 8080` and allows for powerful configuration via `~/.mitmproxy/config.yaml`.
