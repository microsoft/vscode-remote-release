---
description: "Use when editing the workspace Dev Container configuration. Require an explicit user request before changing it."
name: "Dev Container Change Gate"
applyTo: ".devcontainer/devcontainer.json"
---

# Dev Container Configuration Changes

- Do not modify `.devcontainer/devcontainer.json` as part of unrelated work, cleanup, refactoring, or inferred project needs.
- Change this file only when the user's current prompt explicitly requests a change to the Dev Container configuration or to this file.
- Do not treat a request to inspect, explain, or review the configuration as permission to edit it.
- Keep any explicitly requested change limited to its stated scope.
