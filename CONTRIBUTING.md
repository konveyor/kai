# Contributing Guide

- [Contributing Guide](#contributing-guide)
  - [Ways to Contribute](#ways-to-contribute)
    - [Come to Meetings](#come-to-meetings)
  - [Contact Us](#contact-us)
    - [Slack](#slack)
    - [Mailing list](#mailing-list)
  - [Find an Issue](#find-an-issue)
  - [Ask for Help](#ask-for-help)
  - [Pull Request Lifecycle](#pull-request-lifecycle)
  - [Pull Request Title](#pull-request-title)
  - [Development Environment Setup](#development-environment-setup)
  - [Linting](#linting)
  - [Testing](#testing)
  - [Modifying a Python Dependency](#modifying-a-python-dependency)
  - [Running the Project](#running-the-project)
  - [Working with Notebooks](#working-with-notebooks)
  - [Sign Your Commits](#sign-your-commits)
    - [DCO](#dco)
  - [Pull Request Checklist](#pull-request-checklist)

Welcome! We are glad that you want to contribute to our project! 💖

As you get started, you are in the best position to give us feedback on areas of
our project that we need help with including:

- Problems found during setting up a new developer environment
- Gaps in our Quickstart Guide or documentation
- Bugs in our automation scripts

If anything doesn't make sense, or doesn't work when you run it, please open a
bug report and let us know!

## Ways to Contribute

We welcome many different types of contributions including:

- New features
- Builds, CI/CD
- Bug fixes
- Documentation
- Issue Triage
- Answering questions on Slack/Mailing List
- Web design
- Communications / Social Media / Blog Posts
- Release management

Not everything happens through a GitHub pull request. Please come to our
[meetings](#come-to-meetings) or [contact us](#contact-us) and let's discuss how
we can work together.

### Come to Meetings

Please consider joining the [Konveyor community
meetings](https://github.com/konveyor/community?tab=readme-ov-file#konveyor-community-meetings).

Absolutely everyone is welcome to come to any of our meetings. You never need an
invite to join us. In fact, we want you to join us, even if you don’t have
anything you feel like you want to contribute. Just being there is enough!

You can find out more about our meetings
[here](https://github.com/konveyor/community?tab=readme-ov-file#konveyor-community-meetings).
You don’t have to turn on your video. The first time you come, introducing
yourself is more than enough. Over time, we hope that you feel comfortable
voicing your opinions, giving feedback on others’ ideas, and even sharing your
own ideas, and experiences.

## Contact Us

### Slack

You can reach us in kubernetes.slack.com in :

- [#konveyor](https://kubernetes.slack.com/archives/CR85S82A2)
- [#konveyor-dev](https://kubernetes.slack.com/archives/C04QZJFQ0UA)

If you don't already have a slack account for kubernetes.slack.com you can
receive an automatic invite via:
https://communityinviter.com/apps/kubernetes/community

### Mailing list

Subscribe to the [Konveyor emailing
lists](https://groups.google.com/g/konveyor-dev
https://github.com/konveyor/community?tab=readme-ov-file#mailing-lists)

For technical discussions please join/email:

- konveyor-dev@googlegroups.com
  - Konveyor development related issues and general questions
  - Subscribe via: https://groups.google.com/g/konveyor-dev

## Find an Issue

We have good first issues for new contributors and help wanted issues suitable
for any contributor.

- The [good first
  issue](https://github.com/konveyor/kai/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
  tag has extra information to help you make your first contribution.
- The [help wanted](https://github.com/konveyor/kai/labels/help%20wanted) tag has
  issues that are suitable for someone who isn't a core maintainer and is good to
  move onto after your first pull request.

Sometimes there won’t be any issues with these labels. That’s ok! There is
likely still something for you to work on. If you want to contribute but you
don’t know where to start or can't find a suitable issue, you can reach out to
us in [slack](#slack)

Once you see an issue that you'd like to work on, please post a comment saying
that you want to work on it. Something like "I want to work on this" is fine.

## Ask for Help

The best way to reach us with a question when contributing is to ask on:

- The original github issue
- [The developer mailing list](https://groups.google.com/u/1/g/konveyor-dev)
- [Our Slack channel - #konveyor-dev](https://kubernetes.slack.com/archives/C04QZJFQ0UA)

## Pull Request Lifecycle

- Please submit pull-requests for the 'main' branch
- Please link your PR to an existing issue, if an existing issue is not present
  consider creating a new issue
- If the PR is not yet ready you may mark it as a draft, and then once it's
  ready for a review remove the draft status and add a comment to let us know
  you are ready for a review.

## Pull Request Title

Please ensure the title of your PR begins with a
[gitemoji](https://github.com/carloscuesta/gitmoji) such as:

- `:bug:` - For bug fixes
- `:book:` - For documentation
- `:sparkles:` - For new features
- `:seedling:` - For infrastructure related changes
- `:warning:` - For breaking changes
- `:ghost:` - For misc updates/fixes that don't need to show up in release notes

For more info you can consult the pr check we run at
[konveyor/release-tools](https://github.com/konveyor/release-tools/blob/main/pkg/pr/prefix.go)

## Development Environment Setup

See [docs/contrib/dev_environment.md](docs/contrib/dev_environment.md)

## Linting

1. Install trunk via: https://docs.trunk.io/check#install-the-cli
1. Run the linters: `trunk check`
1. Format code: `trunk fmt`

## Testing

- Please include a unit test for new features
- See [docs/contrib/Testing.md](docs/contrib/Testing.md) for more guidance on
  testing

## Modifying a Python Dependency

If you need to add or update a Python dependency in the project, follow these
steps:

1. **Add the dependency**: Open `pyproject.toml` and add the new dependency to
   the `dependencies` list or modify an existing one.

2. **Compile the requirements**: Run the following commands to compile the
   dependencies and update the `requirements.txt` file:

   ```bash
      python -m venv <venv-name>
      source <venv-name>/bin/activate
      pip install pip-tools
      pip-compile --allow-unsafe
      pip install -r requirements.txt
   ```

## Running the Project

1. Setup your development environment as per [docs/contrib/dev_environment.md](/docs/contrib/dev_environment.md)
2. **Demo Interaction**: Read and follow [example/README.md](/example/README.md) to learn how to leverage a python script `example/run_demo.py` which will script interaction with Kai.

   Running `run_demo.py` from the `example` directory is a recommended way for
   developers to interact with the project, allowing you to explore and test the
   workflow. For end users, the standard interaction will be through the IDE
   plugin, which provides the main interface for usage. The `run_demo.py` script
   is an optional method to get a feel for the project.

For end users, please refer to the IDE plugin documentation for the primary interaction path.

## Working with Notebooks

When working with Jupyter notebooks, ensure you've installed the project in
editable mode `pip install -e .` to access all project modules and dependencies.

## Sign Your Commits

### DCO

Licensing is important to open source projects. It provides some assurances that
the software will continue to be available based under the terms that the
author(s) desired. We require that contributors sign off on commits submitted to
our project's repositories. The [Developer Certificate of Origin
(DCO)](https://probot.github.io/apps/dco/) is a way to certify that you wrote and
have the right to contribute the code you are submitting to the project.

You sign-off by adding the following to your commit messages. Your sign-off must
match the git user and email associated with the commit.

```bash
    This is my commit message
    Signed-off-by: Your Name <your.name@example.com>
```

Git has a `-s` command line option to do this automatically:

```bash
    git commit -s -m 'This is my commit message'
```

If you forgot to do this and have not yet pushed your changes to the remote
repository, you can amend your commit with the sign-off by running

```bash
    git commit --amend -s
```

## Pull Request Checklist

When you submit your pull request, or you push new commits to it, our automated
systems will run some checks on your new code. We require that your pull request
passes these checks, but we also have more criteria than just that before we can
accept and merge it. We recommend that you check the following things locally
before you submit your code:

- Ensure that [trunk](https://docs.trunk.io/code-quality/advanced-setup/cli) is happy
  - `trunk check`
  - `trunk fmt`
- Ensure that unit tests pass. See
  [docs/contrib/Testing.md](docs/contrib/Testing.md)
- If adding a new feature please add a new unit test
- If you modified `requirements.txt` please see [Modifying a Python
  Dependency](#modifying-a-python-dependency)
- Ensure that [`example/run_demo.py`](example/run_demo.py) works
- Commits are signed as per [DCO](#dco)
- PR Title begins with a gitemoji as described in [Pull Request
  Title](#pull-request-title)
