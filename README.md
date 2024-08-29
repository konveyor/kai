# Konveyor AI (Kai)

Konveyor AI (Kai) simplifies the process of modernizing application source code to a new platform. It uses Large Language Models (LLMs) guided by static code analysis, along with data from Konveyor. This data provides insights into how similar problems were solved by the organization in the past, helping streamline and automate the code modernization process.

Pronunciation of 'kai': https://www.howtopronounce.com/ka%C3%AC-4

## Approach

Kai implements a [Retrieval Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401) approach that leverages data from Konveyor to help generate code suggestions to aid migrating legacy code bases to a different technology. The intent of this RAG approach is to shape the code suggestions to be similar to how an organization has solved problems in the past, without additional fine-tuning of the model.

The approach begins with using static code analysis via the [Kantra](https://github.com/konveyor/kantra) tool to find areas in the source code that need attention. 'kai' will iterate through analysis information and work with LLMs to generate code changes to resolve incidents identified from analysis.

- Read more about our technical approach here: [docs/Technical_Background.md](docs/design/Technical_Background.md)

- Presentation slides introducing Konveyor AI: [2024_May GenAI Application Migration](https://docs.google.com/presentation/d/1awMdp5hHC6L4Xc_uY6Kj4XiskAArDGPhyQRBI6GJUAo/edit#slide=id.g28c0e0d2936_0_621)

## Demo Video

![DemoVideo](/docs/images/Kai_April_26c.gif)

- See [Generative AI Applied to Application Modernization with Konveyor AI](https://www.youtube.com/watch?v=aE8qNY2m4v4) (~15 minute demo with voice)

## Blog Posts

- 2024 May 07: [Apply generative AI to app modernization with Konveyor AI](https://developers.redhat.com/articles/2024/05/07/modernize-apps-konveyor-ai)
- 2024 May 07: [Kai - Generative AI Applied to Application Modernization](https://www.konveyor.io/blog/kai-deep-dive-2024/)
- 2024 July 23: [Embracing the Future of Application Modernization with KAI](https://shaaf.dev/post/2024-07-23-embracing-the-future-of-app-mod-with-konveyor-ai/)

## Getting Started

1. Run the kai backend image locally with sample data
2. Walk through a guided scenario to evaluate how Kai works

### Launch the Kai backend with sample data

The quickest way to get running is to leverage sample data committed into the Kai repo along with the `podman compose up` workflow

1.  `git clone https://github.com/konveyor/kai.git`
1.  `cd kai`
1.  `git checkout stable`
    - **_NOTE:_** Until we fix [Issue #264](https://github.com/konveyor/kai/issues/264) there is a need to be on `stable` branch of code
1.  Edit `compose.yaml`

        diff --git a/compose.yaml b/compose.yaml
        index c0f2a9e..69a3be8 100644
        --- a/compose.yaml
        +++ b/compose.yaml
        @@ -1,7 +1,7 @@
        version: "3"

        x-kai-variables: &kai-variables
        -  KAI__DEMO_MODE: "False"
        +  KAI__DEMO_MODE: "True"
          HUB_URL: ${HUB_URL:-https://tackle-konveyor-tackle.apps.example.com/hub}
          IMPORTER_ARGS:
          LOG_LEVEL: info

    - **_NOTE:_** The above edit of `compose.yaml` will not be needed once [Issue #257](https://github.com/konveyor/kai/issues/257) is fixed

1.  Run `GENAI_KEY="something" podman compose up`. The first time this is run it will take several minutes to download images and to populate sample data.
    - **_NOTE:_** We need to provide some/any value to `GENAI_KEY` environment variable until we address [Issue #287](https://github.com/konveyor/kai/issues/287)
    - You will need to install [podman](https://podman.io/docs/installation) and [podman-compose](https://github.com/containers/podman-compose?tab=readme-ov-file#installation) if you do not already have it installed. This allows your system to run containers.
    - After the first run the DB will be populated and subsequent starts will be much faster, as long as the kai_kai_db_data volume is not deleted.
    - To clean up all resources run `podman compose down && podman volume rm kai_kai_db_data`.
1.  Kai backend is now running and ready to serve requests

### Guided walk-through

After you have the kai backend running via `podman compose up` you can run through a guided scenario we have to show Kai in action at: [docs/scenarios/demo.md](docs/scenarios/demo.md)

- [docs/scenarios/demo.md](docs/scenarios/demo.md) walks through a guided scenario of using Kai to complete a migration of a Java EE app to Quarkus.

### Others ways to run Kai

The above information is a quick path to enable running Kai quickly to see how it works. If you'd like to take a deeper dive into running Kai against data in Konveyor or your own custom data, please see [docs/Getting_Started.md](docs/Getting_Started.md)

### Debugging / Troubleshooting

- Kai backend will write logging information to the `logs` directory.
  - You can adjust the level via `kai/config.toml` and change the `file_log_level = "debug"` value
- Tracing information is written to disk to aid deeper explorations of Prompts and LLM Results. See [docs/contrib/Tracing.md](docs/contrib/Tracing.md)

## Technical design documents

- See our technical design related information at [docs/design](docs/design)

## Roadmap and Early Builds

- Kai is in it's early development phase and is NOT ready for production usage.
- See [ROADMAP.md](ROADMAP.md) to learn about the project's goals and milestones
- Please see [docs/Evaluation_Builds.md](docs/Evaluation_Builds.md) for information on early builds.

## Contributing

Our project welcomes contributions from any member of our community. To get
started contributing, please see our [Contributor Guide](CONTRIBUTING.md).

## Code of Conduct

Refer to Konveyor's Code of Conduct [here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).
