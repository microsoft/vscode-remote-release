# Dev Containers: VS Code Freezes While Activating Extensions

## Symptoms

When connecting to a Dev Container, VS Code may become unresponsive with the status bar showing "Activating Extensions...". The window stops responding and you may see a dialog indicating "The window is not responding."

In the logs (`main.log`), you may see entries like:
```
[error] CodeWindow: detected unresponsive
```

## Cause

This issue can occur when there are stale port forwarding entries stored in VS Code's database. When VS Code attempts to restore previously forwarded ports on reconnection, it may hang if those ports are no longer available or conflict with ports already exposed by the container.

This is particularly common when:
- Your `devcontainer.json` includes `forwardPorts` configuration
- Your `docker-compose.yml` also exposes the same ports
- The container has been rebuilt or the port configuration has changed

## Workaround

To resolve this issue, you need to clear the cached tunnel restoration entries from VS Code's database.

### Option 1: Using VS Code Developer Tools (Recommended)

1. Open VS Code (on a local folder, not in a Dev Container)
2. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Run **Developer: Open Storage Explorer**
4. Navigate to **Application > IndexedDB > vscode-web-state-db-global > ItemTable**
5. Look for and delete entries with keys starting with:
   - `remote.tunnels.toRestore`
   - `remote.tunnels.toRestoreExpiration`
6. Restart VS Code and try connecting to the Dev Container again

### Option 2: Reset VS Code State

If Option 1 doesn't work, you can reset VS Code's state by clearing its cache:

**On Linux:**
```bash
rm -rf ~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers
```

**On macOS:**
```bash
rm -rf ~/Library/Application\ Support/Code/User/globalStorage/ms-vscode-remote.remote-containers
```

**On Windows:**
```powershell
Remove-Item -Recurse -Force "$env:APPDATA\Code\User\globalStorage\ms-vscode-remote.remote-containers"
```

> **Note:** This will reset all Dev Containers extension state. You may need to reconfigure some settings.

## Prevention

To prevent this issue from recurring:

1. **Avoid duplicate port forwarding**: If ports are already exposed in `docker-compose.yml`, you may not need to also list them in `forwardPorts` in `devcontainer.json`

2. **Use `forwardPorts` OR Docker ports**: Choose one method for exposing ports rather than both

3. **Consider using `appPort`**: In `devcontainer.json`, `appPort` is specifically designed for ports that should always be forwarded, while `forwardPorts` is for ports that VS Code should auto-forward when detected

## Related Issues

- [#9943](https://github.com/microsoft/vscode-remote-release/issues/9943) - Original issue discussing this problem
