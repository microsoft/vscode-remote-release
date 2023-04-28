The Remote-SSH extension is a private repo that other extensions rely on for varying functionality. Below is a list of commands that we will comitt to keeping stable like an API. These commands, now published externally here, will be maintained.



## Remote-SSH Stable Commands:

`opensshremotes.openEmptyWindow` - Opens a new window and attempts to connect to the remote provided through the `args`
- parameters: [`(args?: IOpenWindowsArgs)`](#IOpenWindowsArgs-Definition)
- returns: none
- this command is called with the command palette command "Connect to Host.."

`opensshremotes.openEmptyWindowInCurrentWindow` - Attempts to connect to the remote provided through the `args` argument but in the current VS Code window 
- parameters: [`(args?: IOpenWindowsArgs)`](#IOpenWindowsArgs-Definition)
- returns: none
- this command is called with the command palette command "Connect Current Window to Host..."

## Interface Definitions

##### IOpenWindowsArgs Definition
```
interface IOpenWindowsArgs {
	host: string;
	userName?: string;
	port?: number;
}
```

