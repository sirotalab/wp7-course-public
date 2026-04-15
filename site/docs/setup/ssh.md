# SSH setup

This page walks you through getting onto the lab HPC from your laptop.

!!! info "Source"
    Based on the lab's general SSH onboarding docs at
    `/storage/share/sirocampus/docs/how-to/ssh/ssh-setup.md` (readable once
    you're on the HPC). If this page and the lab docs disagree, trust the lab
    docs.

## Your login account

The cohort shares 10 pooled accounts: **`ephys01` … `ephys10`**. To get yours
assigned, fill in the [SSH access request form](../tools/request-access.html) —
you will receive your `ephysNN` login and initial password by reply.

Multiple students may share the same `ephysNN` login, so filesystem ownership
does **not** identify an individual. See [HPC workspace](workspace.md) for the
per-student subdirectory convention.

## On-campus vs off-campus

- **On-campus** (LMU wired or eduroam): you can `ssh` directly to the lab nodes.
- **Off-campus**: you need the LMU VPN or the x2go tunnel — ask the lab IT
  lead if you need credentials. See
  `/storage/share/sirocampus/docs/handbook/it/remote_access.md` for the
  current procedure.

## 1. Generate an SSH key (once, on your laptop)

=== "Linux / macOS"

    ```bash
    ssh-keygen -t ed25519 -C "your.email@campus.lmu.de"
    ```

    Press Enter to accept the default path (`~/.ssh/id_ed25519`). Choose a
    passphrase if you want extra protection.

=== "Windows (PowerShell or Git Bash)"

    ```powershell
    ssh-keygen -t ed25519 -C "your.email@campus.lmu.de"
    ```

    Keys land in `C:\Users\<you>\.ssh\`.

Use `ed25519` — it's smaller and faster than RSA.

## 2. Configure `~/.ssh/config`

Create or edit `~/.ssh/config` (`C:\Users\<you>\.ssh\config` on Windows) and add:

```
Host gamma3
  HostName 10.153.170.43
  User ephysXX
  Port 22

Host theta
  HostName 10.153.170.1
  User ephysXX
  Port 22

Host beta
  HostName 10.153.170.3
  User ephysXX
  Port 22
```

Replace `ephysXX` with your assigned pooled login. Make sure `~/.ssh` is
permissions `700` (Linux/macOS) — otherwise ssh will refuse to use it.

`theta` is the head node (fine for `cd` / `ls` / light tasks), `gamma1`–`gamma4`
are compute nodes (use these for exercises), and `beta` is the git / datalad
bastion (you only need it for off-HPC `datalad clone`).

## 3. First login with password

```bash
ssh gamma3
```

Enter the initial password (given to you by the course organizers). After the
first login, immediately log out with `exit`.

## 4. Install your public key (so you don't retype the password)

**Preferred — one command:**

```bash
ssh-copy-id gamma3
```

**Manual fallback** if `ssh-copy-id` isn't available:

```bash
# On your laptop — print your public key
cat ~/.ssh/id_ed25519.pub
# Copy the whole line starting with `ssh-ed25519`.

# Then on gamma3
ssh gamma3
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "<paste-your-public-key-here>" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

## 5. Verify the key works

```bash
ssh gamma3
# Should log in without asking for a password.
```

If it still asks for a password, permissions on `~/.ssh` / `authorized_keys`
are probably wrong — re-run the `chmod` commands above.

## Next

Once `ssh gamma3` works passwordless, continue to [VS Code
Remote-SSH](vscode.md) for the recommended way to actually work on notebooks.
