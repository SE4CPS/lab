<!--
  Source: emailed by Jeff (SOECS/lab support) to Sepehr, Tap, and Solomon,
  covering the new Windows 11 SOECS-image lab computers in CTC 214 (the
  ~9-year-old Linux lab machines they replaced). Reused here near-verbatim
  ("with some AI cleanup" per Jeff's note) as a linked student resource for
  COMP-175 Assignment 1 / Practical Lab, in case VirtualBox cannot be
  installed on a given CTC 214 machine without local admin rights. Not
  independently verified by the instructor as of 2026-08-22 -- treat as
  Jeff's field notes, refine as students report successes/failures.
-->

This guide explains how to install and run **Kali Linux with a graphical desktop** on the standard University Windows 11 lab computers using **Windows Subsystem for Linux 2 (WSL2)** and **Kali Win-KeX**.

## Important Notes

- Perform these steps while logged into Windows with your **normal University account**. Do **not** run PowerShell as Administrator.
- WSL2 is already enabled on the lab computers.
- Your Kali installation belongs to **your Windows account on that particular physical computer**.
- Your Kali installation and files under your Linux home directory **do not automatically follow you to another lab computer**.
- You will create a separate Kali username and password. **Do not reuse your University password.**
- Root/`sudo` access inside Kali does **not** make you a Windows administrator.

---

# One-Time Setup

## 1. Open PowerShell

Launch **PowerShell normally**. Do **not** select "Run as administrator."

## 2. Verify WSL2

```powershell
wsl --status
```

Look for `Default Version: 2`. You can also display installed WSL components and versions:

```powershell
wsl --version
```

To see whether you already have a Linux distribution installed:

```powershell
wsl --list --verbose
```

On a fresh account, no Linux distributions may be listed.

## 3. Install Kali Linux

```powershell
wsl --install -d kali-linux
```

If the normal installation is blocked because of Microsoft Store restrictions, this alternative may work:

```powershell
wsl --install --web-download -d kali-linux
```

When Kali initializes, create a **Kali username and password** (separate from your University credentials).

After installation, verify Kali is using WSL2:

```powershell
wsl --list --verbose
```

You should see something similar to:

```text
NAME          STATE     VERSION
kali-linux    Stopped   2
```

## 4. Start Kali

Kali should appear in the Windows Start menu, or start it directly:

```powershell
wsl -d kali-linux
```

---

# Install Kali Tools and the Graphical Desktop

Run the following **inside Kali**, not PowerShell.

```bash
sudo apt update
sudo apt full-upgrade -y
```

Then install useful command-line utilities, Win-KeX, and Kali's standard tool collection:

```bash
sudo apt install -y git curl nmap kali-win-kex kali-linux-default
```

`kali-linux-default` installs approximately the collection of security tools included in Kali's normal default desktop installation. This step can take a while and use significant disk space &ndash; **start it during a lecture day, ahead of when you need it.** Accept default configuration options unless your instructor says otherwise.

---

# Start the Kali Graphical Desktop

```bash
kex --win
```

The first time Win-KeX starts, you will be asked to create a **VNC password** (yet another separate password &ndash; do not reuse your University password). When asked about a **view-only password**, normally answer `N`.

Win-KeX will launch the Kali graphical desktop full-screen (TigerVNC-based Window Mode).

---

# Getting Out of Full-Screen Mode

Press **F8** to open the Win-KeX/TigerVNC menu. From there you can disable **Full screen**, change viewer options, or select **Exit viewer** (closes the viewer but leaves the session running in the background).

---

# Reconnect to an Existing Kali GUI Session

```bash
kex --win --start-client
```

# Stop the Kali GUI Session

```bash
kex --win --stop
```

# Leave Kali and Return to PowerShell

```bash
exit
```

Closing a terminal does not necessarily stop Kali or Win-KeX running in the background.

---

# Useful WSL Commands (from PowerShell)

```powershell
wsl --list --verbose      # show installed distributions
wsl --list --running      # show only running distributions
wsl -d kali-linux         # start Kali
wsl --terminate kali-linux  # stop only Kali
wsl --shutdown            # stop ALL running WSL distributions for your account
```

---

# Updating Kali Later

```bash
sudo apt update
sudo apt full-upgrade -y
```

You generally do **not** need to reinstall Kali to get current software.

---

# Where Are My Files?

Your Kali environment is stored **locally on the physical lab computer**, under your Windows account, e.g. `/home/your-kali-username/`.

> **Do not assume files stored only inside Kali will be available if you sit at a different lab computer next time.** (Assigned seating only, effectively.)

For coursework, store or synchronize files via Git/GitHub, University network storage, OneDrive, or another instructor-approved service.

---

# Accessing Windows Files from Kali

Windows drives are available under `/mnt`, e.g. the C: drive at `/mnt/c`, and your Windows user directory typically at `/mnt/c/Users/YOUR-WINDOWS-USERNAME`. Windows permissions still apply &ndash; `sudo`/root inside Kali does **not** grant Windows Administrator privileges.

---

# If Something Goes Wrong

**KeX GUI running but not visible:** `kex --win --start-client`; if needed, `kex --win --stop` then `kex --win`.

**Kali stuck or won't restart:**

```powershell
wsl --terminate kali-linux
wsl -d kali-linux
```

For a full WSL restart: `wsl --shutdown`, then `wsl -d kali-linux`.

**Forgot the KeX/VNC password:**

```bash
kex --passwd
```

---

# Completely Resetting Kali &ndash; Use with Caution

```powershell
wsl --unregister kali-linux
```

**WARNING:** this permanently deletes the entire Kali distribution &ndash; Linux home directory, installed software, configuration, and all locally stored coursework in it. Not a normal troubleshooting command. Reinstall afterward with `wsl --install -d kali-linux`.

---

# Quick Reference

| Action | Command |
|---|---|
| Start Kali (PowerShell) | `wsl -d kali-linux` |
| Start graphical desktop (inside Kali) | `kex --win` |
| Leave full-screen | F8, then disable Full screen |
| Reconnect to running GUI | `kex --win --start-client` |
| Stop GUI | `kex --win --stop` |
| Exit Kali shell | `exit` |
| Stop Kali (PowerShell) | `wsl --terminate kali-linux` |
| Update Kali | `sudo apt update && sudo apt full-upgrade -y` |
