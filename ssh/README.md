# Remote - SSH

## Baseline Tests

The collection of [dev container](https://containers.dev) configurations in this directory are used during the development and release of the Remote - SSH extension.  This collection will grow along with development of the product, user bug reports, and product goals to generate a set of actionable regression tests.  Internally, a unit testing suite directly employs these configurations and the associated `baseline.json`.

### Testing yourself

To test these configurations yourself against a built of the Remote - SSH extension, perform the following steps. 

1. Install the devcontainer CLI (`npm install -g @devcontainers/cli`). This requires docker on your local machine.
1. Select a configuration and bring the target environment up (`devcontainer up --workspace-folder <PATH_TO_CONFIG>`)
1. These configurations will start an SSH server on a predetermined port addressable on localhost.
1. (Optional) Reconfigure your extension settings to match a scenario within the `baseline.json`.
1. Using the Remote - SSH extension, connect to the container (eg: ssh root@localhost:5678).  The default password is `foobar`.
