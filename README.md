# Kai (Konveyor AI)

<!-- trunk-ignore-begin -->
<div align="center">
  <a href="https://github.com/konveyor/kai">
    <img src="docs/images/kai_logo.png" alt="KAI Logo" width="200" height="200">
  </a>
</div>
<!-- trunk-ignore-end -->

<br>

Kai [(/kaɪ/, rhymes with pie)](https://www.howtopronounce.com/ka%C3%AC-4) - An
AI-enabled tool that simplifies the process of modernizing application source
code to a new platform. It uses **Large Language Models** (LLMs) guided by
**static code analysis**, along with **data from Konveyor**. This data provides
insights into how the organization solved similar problems in the past, helping
**streamline** and **automate** the code modernization process.

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
> adding new features.

Kai began as a Python project in this repository, yet over time it has evolved to be mostly based on Typescript now and as such the majority of the Kai source code exists in the [konveyor/editor-extensions](https://github.com/konveyor/editor-extensions) repository. This repository contains some related components such as the kai_mcp_solution_server and kai_analyzer_rpc.

### 🛠️ Design and Architecture

- [Technical background for our approach](docs/design/technical_background.md)
- [Initial presentation slides introducing
  Kai](https://docs.google.com/presentation/d/1awMdp5hHC6L4Xc_uY6Kj4XiskAArDGPhyQRBI6GJUAo/)
- See other technical design related information at [docs/design](docs/design)

### 🗣️ Conference Talks and Blog Posts

- 2025 April 01: [Project Lightning Talk: Revolutionizing Legacy Migrations with
  Konveyor AI - Jonah Sussman](https://kccnceu2025.sched.com/event/1tcwv)
- 2024 November 22: [Konveyor AI: supporting application
  modernization](https://www.cncf.io/blog/2024/11/22/konveyor-ai-supporting-application-modernization/)
- 2024 August 29: [Incident Storage in Kai - A Deep
  Dive](https://www.konveyor.io/blog/kai-incident-storage-2024/)
- 2024 August 26: [Modernization 101: A Beginner's Guide to Application
  Modernization and Methodology - DevConf.US
  2024](https://www.youtube.com/watch?v=ic5WnbYVTto)
- 2024 July 23: [Embracing the Future of Application Modernization with
  KAI](https://shaaf.dev/post/2024-07-23-embracing-the-future-of-app-mod-with-konveyor-ai/)
- 2024 May 07: [Apply generative AI to app modernization with Konveyor
  AI](https://developers.redhat.com/articles/2024/05/07/modernize-apps-konveyor-ai)
- 2024 May 07: [Deep Dive: Kai - Generative AI Applied to Application
  Modernization](https://konveyor.io/blog/2024/kai-deep-dive-2024/)

### 📽️ Demo Video

![DemoVideo](/docs/images/Kai_April_26c.gif)

[Check out our 15 minute guided demo video to see Kai in
action!](https://www.youtube.com/watch?v=aE8qNY2m4v4)

#### Additional YouTube Videos from Community Members

- [Upgrade your code with AI: Build Your Own Amazon
  Q](https://www.youtube.com/watch?v=IF2xQlii4ws) from [Dean
  Peterson](https://www.linkedin.com/in/deantrepreneur/)

## 🚀 Getting Started

We recommend new users download a [release of
Kai](https://github.com/konveyor/editor-extensions/releases) and then walk
through a guided scenario to get a feel of Kai's potential. We've streamlined
the install experience so you just need to download a `.vsix` file and install
it in your VSCode IDE.

1. Please follow the steps here to proceed with getting started:
   [docs/getting_started.md](docs/getting_started.md)
2. After you have Kai installed we encourage you to run through one of our
   guided scenarios at: [docs/scenarios](docs/scenarios/README.md)

## Documentation

Please see [docs/README.md](docs/README.md) for an overview of our documentation

## 🌐 Contributing

Our project welcomes contributions from any member of our community. To get
started contributing, please see our [Contributor Guide](CONTRIBUTING.md).

## ⚖️ Code of Conduct

Refer to Konveyor's Code of Conduct
[here](https://github.com/konveyor/community/blob/main/CODE_OF_CONDUCT.md).

## 📜 License

This project is licensed under the Apache License 2.0 - see the
[LICENSE](LICENSE) file for details.
