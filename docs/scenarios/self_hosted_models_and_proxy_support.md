# Kai with Self-Hosted Models and Proxies

## Overview

This document explains how to use Kai in scenarios involving proxies, self-hosted models, or both.

## Self-Hosted Models

Many serving runtimes provide an OpenAI compatible API and using any of these options one can host models for use with Kai.

Some examples include text-generation-ui, OpenVino, and vLLM. We have a separate guide for getting started with vLLM on [OpenShift AI with GPU Autoscaling](https://github.com/jmontleon/openshift-ai-with-gpu-autoscaling).

### Use the Kai IDE plugin with OpenShift AI

- Log into the OpenShift cluster, for example:
  `oc login -u kubeadmin https://api.ai.cluster.example.com:6443`

- Obtain the OPENAI_API_KEY, for example:
  `oc get secret -n llms default-name-llama-31-70b-instruct-sa -o go-template='{{ .data.token }}' | base64 -d`

- Obtain the SSL cert for the endpoint with
  `https://llama-31-70b-instruct-llms.apps.ai.cluster.example.com/v1`

- Add the provider to provider-settings.yaml, replacing the SSL_CERT_FILE, REQUESTS_CA_BUNDLE, OPENAI_API_KEY with the appropriate values.

```yaml
rhoai: &active
  environment:
    SSL_CERT_FILE: "/path/to/ca-cert.pem"
    REQUESTS_CA_BUNDLE: "/path/to/ca-cert.pem"
    OPENAI_API_KEY: "token-string"
  provider: "ChatOpenAI"
  args:
    model: "llama-31-70b-instruct"
    base_url: "https://llama-31-70b-instruct-llms.apps.ai.cluster.example.com/v1"
```

- Remember to remove the `&active` anchor tag from other providers.

## Proxy Support

Kai is written in python and capable of functioning through an http(s) proxy using environment variables to adjust the functionality of common python libraries.

mitmproxy is one example of a cross platform, powerful, and easy to use proxy that can be used to demonstrate support.

### Use the Kai IDE plugin with OpenShift AI through a Proxy

- Download the mitmproxy binary appropriate to your system from https://www.mitmproxy.org/downloads/

- Obtain the OPENAI_API_KEY as before, for example:
  `oc get secret -n llms default-name-llama-31-70b-instruct-sa -o go-template='{{ .data.token }}' | base64 -d`

- Extract and run `mitmproxy -p 8443 -k`. `-p` specifies the local port, while `-k` does not attempt to verify the upstream SSL cert.

- The first time mitmproxy runs it generates a CA certificate at `~/.mitmproxy/mitmproxy-ca-cert.pem`

- Add the provider to provider-settings.yaml. To test bearer token override use the string "EMPTY" for `OPENAI_API_KEY` with the appropriate values. Otherwise replace it with the token string you retrieved.

```yaml
rhoai-proxy: &active
  environment:
    SSL_CERT_FILE: "~/.mitmproxy/mitmproxy-ca-cert.pem"
    REQUESTS_CA_BUNDLE: "~/.mitmproxy/mitmproxy-ca-cert.pem"
    OPENAI_API_KEY: "token-string"
    HTTPS_PROXY: "http://localhost:8443"
    HTTP_PROXY: "http://localhost:8443"
    OPENAI_PROXY: "http://localhost:8443"
    PYTHONHTTPSVERIFY: "0"
  provider: "ChatOpenAI"
  args:
    model: "llama-31-70b-instruct"
    base_url: "https://llama-31-70b-instruct-llms.apps.ai.cluster.example.com/v1"
```

- Remember to remove the `&active` anchor tag from other providers.
