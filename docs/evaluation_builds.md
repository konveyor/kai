# Evaluation builds

_Please note that Konveyor AI (Kai) is in early stage of development and is not suitable for production usage at this point in time._

The community is releasing early access builds of Kai to aid end user evaluation purposes.

## What evaluation build (release) should I consume?

The recommended option for previewing Kai is to consume the `:stable` image tag.

The `:stable` tag is a floating tag which will point to the current recommended `:demo.{DATE}` tag.

By default, `podman compose up` workflow with [compose.yaml](https://github.com/konveyor/kai/blob/main/compose.yaml) will consume `:stable`.

## Where can we see existing evaluation builds (releases)?

Releases may found at: https://github.com/konveyor/kai/releases

## What is in an evaluation build (release)?

Releases consist of:

- [Git tag for the kai](https://github.com/konveyor/kai/tags) GitHub repository
- Container image with a tag matching the git tag, published to https://quay.io/repository/konveyor/kai?tab=tags
- A `.vsix` file for the associated [Kai VSCode Plugin Build](https://github.com/konveyor-ecosystem/kai-vscode-plugin/tree/main/builds)

## What are the various choices I have for tags?

- `:stable`

  - The `:stable` tag is a floating tag that will point to a recommended early build

- `:demo.${DATE}`

  - The `:demo.${DATE}` tags correspond to early-access builds which are generated on a frequent basis. These early builds may be unstable, we recommend you consume the `:stable` build unless you have a known reason to do something different.

- `:latest`
  - The `:latest` tag is a floating tag which follows the 'main' branch of the kai repository. This tag is useful if you want to see the very latest developments as they merge.
