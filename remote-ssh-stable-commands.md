The Remote-SSH extension is a private repo that other extensions rely on for varying functionality. Below is a list of commands that we will comitt to keeping stable like an API. These commands, now published externally here, will be maintained and changes will not be made without sufficient warning to allow for other dependent extensions to function correctly.



## Remote-SSH Stable Commands:

`opensshremotes.openEmptyWindow` - Opens a new window and attempts to connect to the remote provided through the `args`
- parameters: [`(args?: IOpenWindowsArgs)`](#IOpenWindowsArgs-Definition)

### My Multi Word Header
- returns: none
- this command is called with the command palette command "Connect to Host.."

`opensshremotes.openEmptyWindowInCurrentWindow` - Attempts to connect to the remote provided through the `args` argument but in the current VS Code window 
- parameters: [`(args?: IOpenWindowsArgs)`](#IOpenWindowsArgs-Definition)
- returns: none
- this command is called with the command palette command "Connect Current Window to Host..."


`opensshremotes.cleanRemoteServer` - This command shuts down and uninstall the VS Code server on the remote. A complete uninstall includes removing the entire folder with the server data. This server data includes logs, the server data needed for future reconnection, any unsaved progress of files on the remote machine, and ...  This command causes the [`interactivelyPickSshHost`](#Interactively-Pick-Ssh-Host) to engage, see below for details on how this picker works.
- parameters: none
- returns: none
- this command is called with the command palette command "Kill VS Code Server on Host..."

`opensshremotes.cleanDevBox` - This command uninstalls the Vs Code server on the remote. This command causes the [`interactivelyPickSshHost`](#Interactively-Pick-Ssh-Host) to engage, see below for details on how this picker works.
- parameters: none
- returns: none
- this command is called with the command palette command "Uninstall VS Code Server from Host..."



## Interface Definitions

##### IOpenWindowsArgs Definition
```
interface IOpenWindowsArgs {
	host: string;
	userName?: string;
	port?: number;
}
```
##### Interactively Pick Ssh Host

`interactivelyPickSshHost` This is an additional function which is called by both `opensshremotes.cleanRemoteServer` and `opensshremotes.cleanDevBox`. This command causes an interactive popup to appear where the user will then select from their list of remotes which one they want to kill the server on. The remotes displayed in the interactive popup are collected from parsing the ssh config file and therefore all remotes listed in the ssh config will be displayed as options.

