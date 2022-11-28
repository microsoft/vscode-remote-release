## Debugging for Remote-SSH

If you are experiencing an issue with Remote-SSH in VS Code please follow these steps to debug yourself before then filing an issue on our repo [here](https://github.com/microsoft/vscode-remote-release/issues/new/choose). Going through these steps before submitting an issue is **required** as it provides additional information that will help debug your issue. Thanks!

1.  Solutions to many common user issues with both Remote-SSH and remote development in VS Code can be found by going to our [troubleshooting docs](https://code.visualstudio.com/docs/remote/troubleshooting). Check there first to see if your problem is a common issue we have a solution to.
2.  Try running your SSH connection command in your local terminal. First you must find the logs by click on the `View` menu at the very top of your computer screen, then select `Output` from the dropdown, and then select `Remote-SSH` from the output dropdown on the top right of the `Output` window. Next search in your SSH logs for `Running ssh connection command` and copy the command directly after. This is the exact command the extension attempted to use. If you are **unable** to connect to your remote machine from the command line this means you **likely have an issue with your SSH** (for example the config file, authorization, or the command you are trying to run). Please look at SSH help docs to troubleshoot your issue in this case.
3.  Now try running this command but add `echo "echo hello" |` to the beginning of your SSH command to confirm that we can execute a script on your remote by piping it into SSH.
4.  Also, try connecting via Remote-SS with all other VS Code extensions disabled. You can disable all extensions by going to the `Extensions` viewlet then clicking the three dot menu and selecting `Disable All Installed Extensions` then re-enabling the Remote-SSH extension. This command can be reversed afterwords by selected `Enable All Extensions` from the same dropdown. If your SSH connection works with all other extensions disabled, it is likely one of your install extensions that is causing a problem.
5. Try connecting with Remote-SSH with both values of the `remote.SSH.useLocalServer` settings as shown below and see if either of them are successful. If both still fail, evaluate if the failure message is different. If you are submitting an issue please record this observation as we will ask you to include it in your bug submission.

### remote.SSH.useLocalServer - Server Mode for Connecting:
The Remote-SSH extension has a setting called `remote.SSH.useLocalServer` which provides two different modes of connecting. The default value is true which is called  `Local Server Mode` and when false it is `Terminal Mode`. This setting by default is disabled on Windows, to enable it on Windows you must enable it directly in your settings.json, not through the settings UI. The two options are described below:
- `Local Server Mode`: The Remote-SSH extension spawns an SSH process via Node which will then be reused by all VS Code windows connected to that remote. This mode allows for a single, shared Remote-SSH connection.
- `Terminal Mode`: In this mode, the Remote-SSH extension runs the SSH connection command in a background terminal. This means each VS Code window has it own connection and therefore it is not a shared connection.



### Other Suggestions:
Here are a few other useful tips which can help reset, find errors, or debug a very specific setup issue.
1.  If you are attempting to "reset" your environment to retry the connection and it seems as though VS Code data is persisting on your remote side, run `Kill Remote Server` on your client side to reset.
2.  Look at the developer tools by going to `Help` in the menu then selecting `Toggle Developer Tools` from the dropdown. Check for errors here because extension startup or other errors might show up here.
3.  Toggle the setting `remote.SSH.localServerDownload` can be useful if you think you might be experiencing problems downloading the VS Code server on the remote side. The setting is described below:

### remote.SSH.localServerDownload - Server Mode for Downloading:
The Remote-SSH extension has another important setting, `remote.SSH.localServerDownload`. The default value is unchecked which is called `Non-Local Server Download` and checked is `Local Server Download`. This setting specifies how the VS Code server will be downloaded on the remote machine. Below are the two options:
- `Non-Local Server Download`: The Remote-SSH extension will attempt to download VS Code on the server directly. 
- `Local Server Download`: The Remote-SSH extension will attempt to download VS Code on the client then transfer it to the host with scp.
