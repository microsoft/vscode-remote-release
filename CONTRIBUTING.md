<!--
Copyright © Microsoft Corporation
All rights reserved.
Creative Commons Attribution 4.0 License (International): https://creativecommons.org/licenses/by/4.0/legalcode
-->

# Contributing to VS Code Remote Development

There are many ways for you to contribute to VS Code Remote Development (WSL, Remote - SSH, Remote - Tunnels, Dev Containers). This document will outline a number of ways you can get involved.

## Reporting Issues

Have you identified a reproducible problem in VS Code Remote extensions? Have a feature request? We want to hear about it! Here's how you can make reporting your issue as effective as possible.

### Identify Where to Report

This repository is specifically for the VS Code Remote Development extension pack and related extensions. Consider these other locations for your feedback if your issue is not directly related to these extensions:

- If you are encountering an issue with another extension when running in a remote environment, please raise an issue in the extension's repository. You can reference the [summary](https://aka.ms/vscode-remote/troubleshooting/extensions) of tips for resolving extension issues and our [extension guide](https://aka.ms/vscode-remote/developing-extensions) to help the extension author get started.
- You can report issues related to offically maintained Dev Container Templates at [devcontainers/templates](https://github.com/devcontainers/templates).
- You can report issues related to offically maintained Dev Container Features at [devcontainers/features](https://github.com/devcontainers/features).
- Image issues for `mcr.microsoft.com/devcontainers` and `mcr.microsoft.com/vscode/devcontainers` images can be raised at [devcontainers/images](https://github.com/devcontainers/images).
- For issues related to the Dev Container specification, raise an issue at [devcontainers/spec](https://github.com/devcontainers/spec).
- For issues related to the Dev Container CLI, raise an issue at [devcontainers/cli](https://github.com/devcontainers/cli).
- Github Codespaces issues should be raised in [GitHub Feedback](https://github.com/github/feedback/discussions/categories/codespaces).
- If you are not looking to report an issue related to these extensions, you may be looking for the [VS Code OSS](https://github.com/Microsoft/vscode) repository. However, note that, the VS Code project is distributed across multiple repositories. See the list of [Related Projects](https://github.com/Microsoft/vscode/wiki/Related-Projects) if you aren't sure which repo is correct.

### Look For an Existing Issue

Before you create a new issue, please do a search in [open issues](https://github.com/Microsoft/vscode-remote-release/issues) to see if the issue or feature request has already been filed.

Be sure to scan through the [most popular](https://github.com/Microsoft/vscode-remote-release/issues?q=is%3Aopen+is%3Aissue+label%3Afeature-request+sort%3Areactions-%2B1-desc) feature requests.

If you find your issue already exists, make relevant comments and add your [reaction](https://github.com/blog/2119-add-reactions-to-pull-requests-issues-and-comments). Use a reaction in place of a "+1" comment:

* 👍 - upvote
* 👎 - downvote

If you cannot find an existing issue that describes your bug or feature, create a new issue using the guidelines below.

### Writing Good Bug Reports and Feature Requests

File a single issue per problem and feature request. Do not enumerate multiple bugs or feature requests in the same issue.

Do not add your issue as a comment to an existing issue unless it's for the identical input. Many issues look similar, but have different causes.

The more information you can provide, the more likely someone will be successful at reproducing the issue and finding a fix.

Please include the following with each issue:

* Version of VS Code
  
* What type of remote connection you were using: SSH, Containers, WSL

* Your operating system  

* The remote operating system you are connecting to

* List of extensions that you have installed

* Reproducible steps (1... 2... 3...) that cause the issue

* What you expected to see, versus what you actually saw

* Images, animations, or a link to a video showing the issue occurring

* A code snippet that demonstrates the issue or a link to a code repository the developers can easily pull down to recreate the issue locally

  * **Note:** Because the developers need to copy and paste the code snippet, including a code snippet as a media file (i.e. .gif) is not sufficient.

* Errors from the Dev Tools Console (open from the menu: Help > Toggle Developer Tools)

* If you are using VS Code Remote - Container support, include your container configuration files if you are able to.

### Final Checklist

Please remember to do the following:

* [ ] Search the issue repository to ensure your report is a new issue

* [ ] Recreate the issue after disabling all extensions

* [ ] Simplify your code around the issue to better isolate the problem

Don't feel bad if the developers can't reproduce the issue right away. They will simply ask for more information!

### Follow Your Issue

Once submitted, your report will go into the a similar [issue tracking](https://github.com/Microsoft/vscode/wiki/Issue-Tracking) workflow that is used for the core VS Code project. Be sure to understand what will happen next, so you know what to expect, and how to continue to assist throughout the process.

### Automated Issue Management

We use a bot to help us manage issues. This bot currently:

* Automatically closes any issue marked `needs-more-info` if there has been no response in the past 7 days.
* Automatically locks issues 45 days after they are closed.

If you believe the bot got something wrong, please open a new issue and let us know.

## Contributing to Documentation

If you want to contribute to our documentation, please submit a pull request (or raise an issue) in the [vscode-docs repository](https://github.com/Microsoft/vscode-docs).

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Thank You!

Your contributions, large or small, make great projects like this possible. Thank you for taking the time to contribute.
