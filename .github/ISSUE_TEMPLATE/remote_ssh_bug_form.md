name: Remote-SSH Bug
description: File a bug/issue for the Remote-SSH extension
title: "[Remote-SSH Bug]: "
labels: ["ssh"]
assignees: "eleanorjboyd"
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
      - label: I have tried both values of the `remote.SSH.useLocalServer` setting
        required: true
      - label: I have tried both values of the `remote.SSH.localServerDownload` setting
        required: true
      - label: My SSH command works from a local terminal 
      - label: I can connect using the Remote-SSH extension on VS Code when all other VS Code extensions are disabled
  - type: textarea
    attributes:
      label: ->
      description: If you did not check any box or if there was a difference in behavior when toggling either user setting please elaborate here.
    validations:
      required: false
  - type: textarea
    attributes:
      label: Versions
      description: You can find the VS Code version with [these steps](https://code.visualstudio.com/docs/supporting/FAQ#_how-do-i-find-the-version.). Your Remote-SSH Extension Version number is located next to the name of the extension in the VS Code marketplace, and will follow the format vX.XX.X.
      value: |
        - VS Code Version:
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
      label: Remote-SSH Log
      description:  To find logs first click on the `View` menu at the very top of your computer screen, and then select `Output` from the dropdown. Finally, select `Remote-SSH` from the dropdown on the top right of the `Output` window. Please make sure to provide the entire log as all output is helpful to our debugging.
      value: |
        <details>
        <summary>Remote-SSH Log</summary>
        <p>

        ```
        [PASTE LOG HERE]
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