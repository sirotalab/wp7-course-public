# VS Code Remote-SSH setup

!!! warning "Draft"
    Pull the current content from the sirocampus shared clone before cohort start:

    - `/storage/share/sirocampus/docs/how-to/ssh/vscode-setup.md`
    - `/storage/share/sirocampus/docs/reference/server/vscode-remote.md`
    - `/storage/share/sirocampus/docs/handbook/data/processing/remote_ide.md`

The short version: install the "Remote — SSH" extension, configure your
`~/.ssh/config` with the lab's preferred host/proxy settings, then
"Remote-SSH: Connect to Host".

## Where to land

| Task | Node |
|---|---|
| I/O-heavy file operations | `beta` or `theta` |
| Running notebooks for exercises | `gamma1`–`gamma4` |

Avoid doing heavy file copies on the gamma compute nodes — they're for jobs.
