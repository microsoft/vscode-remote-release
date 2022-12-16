The Remote-SSH extenions is a private repos that other extensions rely on for varying functionality. Below is a list of commands that we will do our best to keep stable similar to an API. These commands, now published externally here, will be maintained and changes will not be made without sufficent warning to allow for other dependent extensions to function correctly.


## Remote-SSH Stable Commands:

#### `opensshremotes.openEmptyWindow`
- parameters: `(args?: IOpenWindowsArgs)` _(see IOpenWindowsArgs definition below)_
- this command is called with the command palette command `Connect to Host..`

#### `opensshremotes.openEmptyWindowInCurrentWindow`
- parameters: `(args?: IOpenWindowsArgs)` _(see IOpenWindowsArgs definition below)_
- this command is called with the command palette command "Connect Current Window to Host..."


#### `opensshremotes.cleanRemoteServer`
- parameters: none
- this command is called with the command palette command "Kill VS Code Server on Host..."

#### `opensshremotes.cleanDevBox`
- parameters: none
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


