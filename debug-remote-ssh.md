## Debugging for Remote-SSH

If you are experiencing a bug with Remote-SSH in VS Code please follow these steps to debug yourself before then filing an issue on our repo [here](https://github.com/microsoft/vscode-remote-release/issues/new/choose). Going through these steps before submitting an issue is **required** as it provides additional information that will help debug your issue. Thanks!

1.  Many of our common issues with both Remote-SSH and remote development in VS Code can be found by going to our [troubleshooting docs](https://code.visualstudio.com/docs/remote/troubleshooting). Check there first to see if your problem is a common issue we have a solution to.
2.  Try running your SSH connection command in your local terminal or powershell. If you are **unable** to connect to your remote machine from the command line this means you **likely have an issue with your SSH** (for example the config file, authorization, or the command you are trying to run). Please look at SSH help docs to troubleshoot your issue in this case.
3.  Now, try running your SSH connection locally **and** disable all extensions. If your SSH connection still does not work when you try the same command this way, it likely relates to a extension issue.
4. Try running your remote-SSH connect with both **server mode** settings as exampled below and see if one is successful. If both still fail, evaluate if the failure message is different. If you are submitting an issue please record this observation as we will ask you to include it in your bug submission.

### Server Mode:
The Remote-SSH extension has two different modes of connect, `Local Server Mode` and `Non-Local Server Mode`. This setting called `remote.SSH.useLocalServer` and its default value is auto where it first attempts `Non-Local Server Mode` and if this fails will try `Local Server Mode`. The difference is as follows:
- `Local Server Mode`: The remote-SSH extension will attempt to download VS Code on the client then transfer it to the host with scp. Spawn and reuse the connection between windows
- `Non-Local Server Mode`: The remote-SSH  extension will attempt to download VS Code on the host directly. Run ssh terminal



### Other Suggestions:
These are non-required suggestions in order to submit a bug to our repo but are the most common fixes for most people when they do reach out.
1.  If you are attempting to "reset" your environment to retry the connection and it seems as though VS Code data is persisting on your remote side, run `Kill Remote Server` on your client side to reset.
2.  If you are struggling with understand if you connection is set up correctly, we suggest using `echo 'hello'` in your ssh connection command as this helps you ping the server and get a simple response.
3.  Look at developer tools by going to `developer tools` on the command palette and checking for errors here. Extension startup or other errors might show up here.