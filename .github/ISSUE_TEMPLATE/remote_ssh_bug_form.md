name: Remote-SSH Bug
description: File a bug/issue for the Remote-SSH extension
title: "[Remote-SSH Bug]: "
labels: ["ssh"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for filling out a bug report and helping improve the Remote-SSH extension! 
        If you have a feature request for Remote-SSH please use the general `Feature request` issue creation button on the previous page.
  - type: checkboxes
    attributes:
      label: Is there an existing issue for this bug?
      description: Please search to see if an issue already exists for the bug you encountered.
      options:
      - label: I have searched the existing issues
        required: true 
  - type: checkboxes
    attributes:
      label: Debugging Steps 
      description: Please go through this debugging help document and follow all the required steps, https://code.visualstudio.com/docs/remote/troubleshooting.
      options:
      - label: I have followed these debugging steps
        required: true
      - label: I have tried both settings of `remote.SSH.useLocalServer`
        required: true
      - label: My SSH command works from a local terminal 
      - label: My SSH command works from a local terminal with extensions disabled
  - type: textarea
    attributes:
      label: Versions
      description: 
      value: |
        - VSCode Version:
        - Local OS Version:
        - Remote OS Version:
    validations:
      required: true
  - type: textarea
    attributes:
      label: Expected Behavior
      description: A concise description of what you expected to happen.
    validations:
      required: false
  - type: textarea
    attributes:
      label: Steps To Reproduce
      description: Steps to reproduce the behavior.
      placeholder: |
        1. In this environment...
        2. With this config...
        3. Run '...'
        4. See error...
    validations:
      required: false
  - type: textarea
    attributes:
      label: Remote-SSH Logs
      description:  You can find them through going to `output` channel in your remote VS Code window then selecting the `remote-ssh` from the dropdown on the right. Please make sure to provide the ENTIRE logs as all output is helpful to our debugging.
      value: |
        <details>
        <summary>User Settings</summary>
        <p>

        ```
        [PASTE LOGS HERE]
        ```

        </p>
        </details>
    validations:
      required: true
  - type: textarea
    attributes:
      label: Anything else?
      description: |
        Links? References? Anything that will give us more context about the issue you are encountering!
  
        Tip: You can attach images or log files by clicking this area to highlight it and then dragging files in.
    validations:
      required: false
