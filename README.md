# Kai (Konveyor AI)

<!-- trunk-ignore-begin -->
<div align="center">
  <a href="https://github.com/konveyor/kai">
    <img src="docs/images/kai_logo.png" alt="KAI Logo" width="200" height="200">
  </a>
</div>
<!-- trunk-ignore-emd -->

<br>

Kai [(/kaɪ/, rhymes with pie)](https://www.howtopronounce.com/ka%C3%AC-4) - An
AI-enabled tool that simplifies the process of modernizing application source
code to a new platform. It uses **Large Language Models** (LLMs) guided by
**static code analysis**, along with **data from Konveyor**. This data provides
insights into how the organization solved similar problems in the past, helping
**streamline** and **automate** the code modernization process.

- [📖 Explore the docs!](/docs)
- [💻 Run through a demo!](/docs/scenarios/demo.md)
- [📈 View the Roadmap!](ROADMAP.md)

## 🔍 About The Project

Kai is an AI-enabled tool that assists with modernizing applications. Kai is
designed to help developers write code more efficiently by providing suggestions
and solutions to common problems. It does this by performing [Retrieval
Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401), working with LLMs
by using [Konveyor](https://github.com/konveyor) analysis reports about the
codebase and generating solutions based on previously solved examples.

Now, you may be thinking: _How is Kai different than other generative AI tools?_

### 1. Kai uses Konveyor’s analysis reports

Konveyor generates analysis reports via
[Kantra](https://github.com/konveyor/kantra) throughout a migration. This
history of reports tells you what’s wrong with your codebase, where the issues
are, and when they happened. This functionality exists today, and developers are
already using this data to make decisions. And because of our RAG approach, this
is all possible _without additional fine-tuning_.

### 2. Kai learns throughout a migration

As you migrate more pieces of your
codebase with Kai, it can learn from the data available, and get better
recommendations for the next application, and the next, and so on. This shapes
the code suggestions to be similar to how your organization has solved problems
in the past.

### 3. Kai is focused on migration

LLMs are very powerful tools, but without explicit guidance, they can generate a
lot of garbage. Using Konveyor’s analysis reports allows us to focus Kai’s
generative power on the specific problems that need to be solved. This pointed,
specific data is the key to unlocking the full potential of large language
models.

## 🏫 Learn More

> [!NOTE]
>
> Kai is in early development. We are actively working on improving the tool and
> adding new features. If you are interested in contributing to the project,
> please see our [Contributor Guide](CONTRIBUTING.md).

### 🗺️ Roadmap and Early Builds

- See [ROADMAP.md](ROADMAP.md) to learn about the project's goals and milestones
- See [docs/evaluation_builds.md](docs/evaluation_builds.md) for information on
  early builds.

### 🛠️ Design and Architecture

- [Technical background for our approach](docs/design/technical_background.md)
- [Initial presentation slides introducing
  Kai](https://docs.google.com/presentation/d/1awMdp5hHC6L4Xc_uY6Kj4XiskAArDGPhyQRBI6GJUAo/)
- See other technical design related information at [docs/design](docs/design)

### 🗣️ Blog Posts

- 2024 August 29: [Incident Storage in Kai - A Deep Dive](https://www.konveyor.io/blog/kai-incident-storage-2024/)
- 2024 July 23: [Embracing the Future of Application Modernization with KAI](https://shaaf.dev/post/2024-07-23-embracing-the-future-of-app-mod-with-konveyor-ai/)
- 2024 May 07: [Apply generative AI to app modernization with Konveyor AI](https://developers.redhat.com/articles/2024/05/07/modernize-apps-konveyor-ai)
- 2024 May 07: [Kai - Generative AI Applied to Application Modernization](https://www.konveyor.io/blog/kai-deep-dive-2024/)

### 📽️ Demo Video

![DemoVideo](/docs/images/Kai_April_26c.gif)

[Check out our 15 minute guided demo video to see Kai in
action!](https://www.youtube.com/watch?v=aE8qNY2m4v4)

## 🚀 Getting Started

There are two elements to Kai that is necessary for it to function: the
**backend** and the **IDE extension**. The backend is responsible for connecting
to your LLM service, ingesting static analysis reports, and generating
solutions. The IDE extension is where you can interact with Kai, see
suggestions, and apply them to your codebase.

### Prerequisites

1. [Git](https://git-scm.com/downloads)
1. A container engine such as [podman](https://podman.io/docs/installation) or
   [docker](https://docs.docker.com/get-docker/). We will provide instructions
   for podman.
1. Docker-compose or Podman-compose, either one will work. For podman-compose,
   you can install it [here](https://github.com/containers/podman-compose).

### Launch the Kai backend with sample data

> [!IMPORTANT]
>
> Kai is in early development and is not yet ready for production use. We
> currently recommend checking out the git tag `stable` for the most stable user
> experience.

The quickest way to get running is to leverage sample data committed into the
Kai repo along with the `podman compose up` workflow

1. `git clone https://github.com/konveyor/kai.git`
1. `cd kai`
1. `git checkout stable`
1. Make sure the podman runtime is running with `systemctl --user start podman`
1. Make sure the `logs` directory accessible to the podman container with
   `podman unshare chown -R 1001:0 logs`
   - This is necessary to allow podman to write to the `logs` directory outside
     the container.
   - Use `sudo chown -R <your_user>:<your_user> logs` to change the ownership
     of the `logs` directory back to your user when done.
1. Run `podman compose up`.
   - The first time this is run it will take several minutes to download images
     and to populate sample data.
   - After the first run the DB will be populated and subsequent starts will be
     much faster, as long as the kai_kai_db_data volume is not deleted.
   - To clean up all resources run `podman compose down && podman volume rm
kai_kai_db_data`.
   - This will run Kai in demo mode, which will use cached LLM responses, via
     setting the environment variable `KAI__DEMO_MODE=true`. To run without demo
     mode execute `KAI__DEMO_MODE=false podman compose up`. See
     [docs/contrib/configuration.md](docs/contrib/configuration.md) for more
     information on demo mode.

The Kai backend is now running and ready to serve requests!

### Guided Walk-through

After you have the kai backend running via `podman compose up` you can run
through a guided scenario we have to show Kai in action at
[docs/scenarios/demo.md](docs/scenarios/demo.md). This document walks through a
guided scenario of using Kai to complete a migration of a Java EE app to
Quarkus.

### Other ways to run Kai

The above information is a quick path to enable running Kai quickly to see how
it works. If you'd like to take a deeper dive into running Kai against data in
Konveyor or your own custom data, please see
[docs/getting_started.md](docs/getting_started.md)

### Debugging / Troubleshooting

- Kai backend will write logging information to the `logs` directory. You can
  adjust the level via the environment variables. For example:
  `KAI__FILE_LOG_LEVEL="debug"`.
- Tracing information is written to disk to aid deeper explorations of Prompts
  and LLM Results. See [docs/contrib/tracing.md](docs/contrib/tracing.md)

## 🌐 Contributing

Our project welcomes contributions from any member of our community. To get
started contributing, please see our [Contributor Guide](CONTRIBUTING.md).

## ⚖️ Code of Conduct

Refer to Konveyor's Code of Conduct
[here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).


## 📜 License

This project is licensed under the Apache License 2.0 - see the
[LICENSE](LICENSE) file for details.
