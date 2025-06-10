# Podman Desktop

## Install

Installation will vary depending on your operating system and distribution and is documented on the Podman Desktop website.

https://podman-desktop.io/docs/installation

## Configuration

- Start Podman Desktop
  <img src="images/podman-desktop-dashboard.png" alt="Podman Desktop Dashboard Image"/>
- Navigate to the Extensions
- Select the Catalog
- Search for `Podman AI Lab`
  <img src="images/podman-desktop-extensions.png" alt="Podman Desktop Extensions Image"/>
- Install the `Podman AI Lab` Extension
- Navigate to the AI Lab
- Under Models select Catalog
  <img src="images/podman-ai-model-catalog.png" alt="Podman AI Model Catalog Image"/>
- Download one or more models
- Navigate to Services
- Click `New Model Service`
  <img src="images/podman-ai-create-service.png" alt="Podman AI Create Service Image"/>
- Select a model to serve and click Create Service
- On the Service details page note the server URL to use with Kai
  <img src="images/podman-ai-service-details.png" alt="Podman AI Service Details Image"/>
- Export the URL, for example `export OPENAI_API_BASE="http://localhost:35841/v1"`
- Note that the Podman Desktop service endpoint is not passworded, but the
  OpenAI library expects `OPENAI_API_KEY` to be set. In this case the value does
  not matter.

## Kai's `provider-settings.yaml` example

```yaml
podman_mistral:
    provider: "ChatOpenAI"
     environment:
      OPENAI_API_KEY: "unused value"
    args:
      model: "mistral-7b-instruct-v0-2"
      base_url: "http://localhost:35841/v1"
```

- Note above `base_url` and `model` need to be updated to match what you have deployed in podman

## Known Issues

- We have experienced problems due to the model context being too short for our inputs with some models. [It is currently possibly, though somewhat difficult to workaround this issue](https://github.com/containers/podman-desktop-extension-ai-lab/issues/1074).
