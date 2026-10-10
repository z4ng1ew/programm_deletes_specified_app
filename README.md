# README.md

```markdown
# uninstall_app

A small tool that fully removes an application from your system.

Works on:
- Ubuntu, Debian, Linux Mint (uses `apt` / `dpkg`)
- Fedora, RHEL, CentOS, Rocky, AlmaLinux (uses `dnf` / `rpm`)

One command removes:
- the program itself
- its system config files
- unused dependencies
- the user's personal files (config, cache, local data)
- the package manager cache

---

## What it can do

- Finds out which package manager your system uses (apt or dnf) — automatically
- Removes the package and its system configs
- Removes dependencies that are no longer needed
- Removes personal files from your home folder:
  - `~/.config/<name>`
  - `~/.cache/<name>`
  - `~/.local/share/<name>`
- Cleans the package manager cache
- Checks that nothing is left behind
- Asks for confirmation before doing anything dangerous
- Can be run with a short `make` command

---

## What you need

- Linux (Ubuntu/Debian or Fedora/RHEL family)
- Python 3 (already installed on both systems by default)
- `sudo` rights

No extra packages to install.

---

## Files

Put these two files in the same folder:

```
uninstall_app.py    # the main script
Makefile            # shortcuts
```

---

## First-time setup

Open a terminal in that folder and run:

```bash
make
```

This makes the script executable. That's it.

If you don't want to use `make`, do this instead:

```bash
chmod +x uninstall_app.py
```

---

## How to use

### With make (easy way)

```bash
# Remove a program
make delete <package_name>

# Examples
make delete firefox
make delete vlc
make delete sublime-text

# Let the script ask you for a name
make run

# Show help
make help

# Remove temporary Python files
make clean
```

### Without make

```bash
sudo ./uninstall_app.py <package_name>

# Or run it and type the name when asked
sudo ./uninstall_app.py
```

> You need `sudo` because the script talks to the system package manager.

---

## What happens when you run it

Step by step:

1. The script checks if your system uses `apt` or `dnf`.
2. It checks if the package is installed.
3. It shows you information about the package.
4. It asks: "Do you want to continue?" — answer `y` or `n`.
5. It removes the package:
   - Ubuntu: `apt purge -y <package>`
   - Fedora: `dnf remove -y <package>`
6. It removes unused dependencies:
   - Ubuntu: `apt autoremove --purge -y`
   - Fedora: `dnf autoremove -y`
7. It asks if you want to remove your personal files for that program.
8. It asks if you want to clean the package manager cache.
9. It checks that the package is gone.

You can say **no** to any step. Nothing is removed without your permission.

---

## Example run (Ubuntu)

```
$ make delete sublime-text
Package manager: apt / dpkg

=== Info about 'sublime-text' ===
  Package: sublime-text
  Version: 4200
  Description: Sublime Text editor

⚠ This will remove 'sublime-text' and its system configs.
Continue? [y/N]: y

$ apt purge -y sublime-text
$ apt autoremove --purge -y

Remove personal config and cache? [Y/n]: y
  Found: /home/user/.config/sublime-text
    Remove /home/user/.config/sublime-text? [y/N]: y
    Removed.

Clean package manager cache? [Y/n]: y

=== Checking for leftovers ===
  ✅ Package removed from dpkg.

✅ Done.
```

## Example run (Fedora)

```
$ make delete firefox
Package manager: dnf / rpm

=== Info about 'firefox' ===
  Name         : firefox
  Version      : 128.3.0
  Summary      : Mozilla Firefox Web browser

⚠ This will remove 'firefox' and its system configs.
Continue? [y/N]: y

$ dnf remove -y firefox
$ dnf autoremove -y

Remove personal config and cache? [Y/n]: y
Clean package manager cache? [Y/n]: y

=== Checking for leftovers ===
  ✅ Package removed from rpm.

✅ Done.
```

---

## Commands used behind the scenes

| Task                  | Ubuntu (apt)                  | Fedora (dnf)            |
|-----------------------|-------------------------------|-------------------------|
| Check if installed    | `dpkg -s <pkg>`               | `rpm -q <pkg>`          |
| Remove package        | `apt purge -y <pkg>`          | `dnf remove -y <pkg>`   |
| Remove dependencies   | `apt autoremove --purge -y`   | `dnf autoremove -y`     |
| Clean cache           | `apt clean && apt autoclean`  | `dnf clean all`         |
| Check leftovers       | `dpkg -l <pkg>`               | `rpm -q <pkg>`          |

---

## How to find the exact package name

If you don't know the exact name, search for it first.

### Ubuntu

```bash
apt list --installed | grep -i <part_of_name>
dpkg -l | grep -i <part_of_name>
```

### Fedora

```bash
dnf list installed | grep -i <part_of_name>
rpm -qa | grep -i <part_of_name>
```

Example:

```bash
rpm -qa | grep -i chrome
```

---

## Safety notes

- ⚠️ **Do not remove system packages.** Examples: `systemd`, `apt`, `dnf`, `glibc`, `libc6`, the Linux kernel.
  Removing them can break your system.
- This tool is meant for normal apps: browsers, editors, media players, messengers.
- Every dangerous step needs your `y` confirmation.
- Personal files are only removed if you say `y` to that question.
- `sudo` is required, because the system package manager needs root.

---

## Common problems

**1. "Package is not installed"**
The package may already be gone, or the name is wrong.
Use the search commands above to find the correct name.

**2. The script didn't find my personal files**
The folder name may not match the package name.
Example: package `google-chrome-stable`, but folder `~/.config/google-chrome`.
Check manually:

```bash
ls ~/.config | grep -i <part_of_name>
ls ~/.cache  | grep -i <part_of_name>
```

**3. "Permission denied"**
Run with `sudo`. The `make delete` target already uses `sudo` inside.

**4. Fedora: `dnf remove` says "No match" but the app is installed**
Sometimes a package is in rpm but not in dnf (installed by hand).
Check:

```bash
rpm -q <pkg>
sudo rpm -e <pkg>
```

---

## Project structure

```
.
├── uninstall_app.py    # the main script
├── Makefile            # short commands
└── README.md           # this file
```

---
