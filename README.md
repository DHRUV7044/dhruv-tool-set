# Dhruv Tool Set Launcher

A lightweight shell launcher for starting `dhruv_tool_set.py` from anywhere in the terminal.

The launcher automatically finds the Python tool-set application, remembers its location when requested, and uses the remembered path on future runs.

---

## Features

- Run `dhruv_tool_set.py` from any directory.
- Check a previously saved Python-file path.
- Check the current/given directory.
- Search the user's home directory when the file is not found.
- Show the full path when a copy is discovered.
- Ask before running a discovered copy.
- Ask separately whether the path should be remembered.
- Store the selected path in a hidden file in the user's home directory.
- Automatically remove the stored path if the file no longer exists.
- Does not require Python code to be modified when the Python file is moved.
- Uses only standard POSIX shell utilities and Python 3.

---

# Project Structure

A typical installation can look like this:

```text
dhruv-tool-set/
├── dhruv_tool_set.py
├── dhruv
└── README.md
```

The launcher script can have any name. For example:

```text
dhruv
```

The important file is:

```text
dhruv_tool_set.py
```

---

# How It Works

The launcher follows a simple search order.

```text
                 Start
                   │
                   ▼
        Is a saved path available?
              │           │
             Yes          No
              │            │
              ▼            ▼
       Does file exist?   Check given/current
          │       │       directory
         Yes      No           │
          │       │            │
          ▼       ▼            ▼
        RUN     Search      Found?
                 again       │
                            │
                       ┌────┴────┐
                      Yes       No
                       │         │
                       ▼         ▼
                    Ask user   Search HOME
                                  │
                                  ▼
                              Found file?
                              │       │
                             Yes      No
                              │       │
                              ▼       ▼
                         Ask to run  Not found
                              │
                              ▼
                         Ask to store
                              │
                              ▼
                             RUN
```

---

# Search Order

The launcher checks locations in this order:

## 1. Previously stored path

The launcher first checks:

```text
$HOME/.dhruv_tool_set_path
```

For a user named `dhruv`, this normally means:

```text
/home/dhruv/.dhruv_tool_set_path
```

If the file exists and contains a valid path, the launcher runs that Python file immediately.

Example contents:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

No questions are required.

---

## 2. Given directory

If no valid stored path exists, the launcher checks the directory supplied as an argument.

For example:

```bash
./dhruv /home/dhruv/dhruv-tool-set
```

It checks:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

If no directory is supplied, it uses the current directory:

```bash
./dhruv
```

which means:

```text
BASE_DIR=$PWD
```

---

## 3. Search the HOME directory

If the Python file is not found in the stored location or given directory, the launcher searches:

```text
$HOME
```

for:

```text
dhruv_tool_set.py
```

For example:

```text
/home/dhruv/projects/dhruv_tool_set.py
/home/dhruv/tools/dhruv_tool_set.py
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

The results are sorted before they are presented.

---

# First Run

Suppose the launcher finds:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

It can display:

```text
Found tool set file:
  /home/dhruv/dhruv-tool-set/dhruv_tool_set.py

Run this file? [Y/n]:
```

Enter:

```text
y
```

or simply press:

```text
Enter
```

The launcher then asks:

```text
Store this path for future use? [Y/n]:
```

If you answer:

```text
y
```

the path is saved.

---

# Stored Path

The launcher stores the selected path in:

```text
$HOME/.dhruv_tool_set_path
```

For example:

```text
/home/dhruv/.dhruv_tool_set_path
```

The file contains only one line:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

This is intentionally a very simple storage mechanism.

It is not a database.

It is just a text file containing the path to the Python application.

---

# Why Is `.dhruv_tool_set_path` Hidden?

On Linux and Unix-like systems, files beginning with `.` are conventionally hidden.

Therefore:

```text
.dhruv_tool_set_path
```

will normally not appear with:

```bash
ls
```

Use:

```bash
ls -la
```

to see it.

You can also inspect the saved path with:

```bash
cat ~/.dhruv_tool_set_path
```

Example:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

---

# Installation

## 1. Place the Python application

For example:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

---

## 2. Create the shell launcher

Create a file such as:

```text
dhruv
```

and place the launcher script inside it.

Make it executable:

```bash
chmod +x dhruv
```

---

## 3. Test it locally

From the directory containing the launcher:

```bash
./dhruv
```

---

# Run From Anywhere

To make the launcher available as a normal terminal command, place it in a directory included in your `PATH`.

A recommended location is:

```text
~/.local/bin
```

Create the directory if necessary:

```bash
mkdir -p ~/.local/bin
```

Copy the launcher:

```bash
cp dhruv ~/.local/bin/dhruv
```

Make it executable:

```bash
chmod +x ~/.local/bin/dhruv
```

---

## Add `~/.local/bin` to PATH

For Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Then reload your shell:

```bash
source ~/.bashrc
```

For Zsh:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

Then:

```bash
source ~/.zshrc
```

Check:

```bash
which dhruv
```

You should see something similar to:

```text
/home/dhruv/.local/bin/dhruv
```

---

# Usage

## Start normally

```bash
dhruv
```

The launcher uses the current directory as the first search location.

---

## Specify a directory

You can provide a directory:

```bash
dhruv /home/dhruv/dhruv-tool-set
```

The launcher checks:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

---

## Run From Any Directory

After installation, you can do:

```bash
cd ~/Documents
dhruv
```

or:

```bash
cd ~/projects
dhruv
```

or:

```bash
cd /tmp
dhruv
```

The launcher does not depend on the directory from which it was started.

---

# Example Workflow

Assume:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

exists.

You run:

```bash
cd ~/Downloads
dhruv
```

The launcher doesn't find the Python file in:

```text
/home/dhruv/Downloads/dhruv_tool_set.py
```

It then searches your home directory.

It finds:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

It asks:

```text
Found tool set file:

  /home/dhruv/dhruv-tool-set/dhruv_tool_set.py

Run this file? [Y/n]:
```

You enter:

```text
y
```

Then:

```text
Store this path for future use? [Y/n]:
```

You enter:

```text
y
```

The launcher creates:

```text
/home/dhruv/.dhruv_tool_set_path
```

with:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

It then starts the Python application.

---

# Future Runs

The next time you execute:

```bash
dhruv
```

the launcher checks:

```text
/home/dhruv/.dhruv_tool_set_path
```

and reads:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

If that file still exists, it launches it directly.

Therefore, you don't have to search for the Python file every time.

---

# Moving the Python Application

Suppose the application is moved from:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

to:

```text
/home/dhruv/projects/dhruv-tool-set/dhruv_tool_set.py
```

The stored file still contains the old path.

The launcher checks the stored path:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

If it doesn't exist anymore, the launcher removes the old stored path:

```text
/home/dhruv/.dhruv_tool_set_path
```

It then searches `$HOME` again.

If it finds:

```text
/home/dhruv/projects/dhruv-tool-set/dhruv_tool_set.py
```

you can choose to save the new path.

---

# Removing the Stored Path

To forget the saved location:

```bash
rm ~/.dhruv_tool_set_path
```

The next time you run:

```bash
dhruv
```

the launcher will search again.

You can check whether the file exists:

```bash
ls -la ~/.dhruv_tool_set_path
```

---

# Checking the Stored Path

Use:

```bash
cat ~/.dhruv_tool_set_path
```

Example:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

If the file doesn't exist:

```text
cat: /home/dhruv/.dhruv_tool_set_path: No such file or directory
```

then no path has been saved yet.

---

# Python Requirement

The launcher requires Python 3.

Check your installation:

```bash
python3 --version
```

Example:

```text
Python 3.12.3
```

The launcher starts the application using:

```bash
python3 /path/to/dhruv_tool_set.py
```

---

# Shell Requirement

The launcher uses:

```sh
#!/bin/sh
```

and standard POSIX shell features.

It uses commands such as:

```text
cat
find
sort
rm
pwd
```

These are normally available on Linux and other Unix-like systems.

---

# Security Considerations

The launcher searches inside:

```text
$HOME
```

for a file named:

```text
dhruv_tool_set.py
```

If multiple copies exist, the launcher displays their full paths and asks before running them.

Do not save a path unless you trust the Python file.

The stored file:

```text
~/.dhruv_tool_set_path
```

contains only a path. It does not contain the Python program itself.

---

# Multiple Copies

If several copies exist:

```text
/home/dhruv/project1/dhruv_tool_set.py
/home/dhruv/project2/dhruv_tool_set.py
/home/dhruv/tools/dhruv_tool_set.py
```

the launcher processes them one at a time.

For each one it can ask:

```text
Found tool set file:
  /home/dhruv/project1/dhruv_tool_set.py

Run this file? [Y/n]:
```

If you choose not to run it, the launcher continues to the next match.

If you run one, it then asks whether the path should be stored.

---

# Design

The launcher has two separate responsibilities.

## Shell launcher

The shell script handles:

- Finding the Python application
- Remembering its location
- Asking for confirmation
- Starting Python

## Python application

`dhruv_tool_set.py` handles the actual tool-set functionality.

This separation means the launcher does not need to know what the Python program does.

---

# Data Flow

```text
                    dhruv
                      │
                      ▼
             Check ~/.dhruv_tool_set_path
                      │
             ┌────────┴────────┐
             │                 │
           Valid            Invalid/
             │              Missing
             │                 │
             ▼                 ▼
          Run Python     Check current/
                         given directory
                              │
                              ▼
                         Search $HOME
                              │
                              ▼
                         Find Python file
                              │
                              ▼
                         Ask to run
                              │
                              ▼
                         Ask to store
                              │
                              ▼
                       ~/.dhruv_tool_set_path
                              │
                              ▼
                       Run Python file
```

---

# Configuration

The main variables are at the beginning of the script:

```sh
TARGET_FILE="dhruv_tool_set.py"
STORE_FILE="$HOME/.dhruv_tool_set_path"
BASE_DIR="${1:-$PWD}"
SEARCH_ROOT="$HOME"
```

## `TARGET_FILE`

The Python file the launcher searches for:

```sh
TARGET_FILE="dhruv_tool_set.py"
```

## `STORE_FILE`

The file used to remember the selected Python path:

```sh
STORE_FILE="$HOME/.dhruv_tool_set_path"
```

## `BASE_DIR`

The directory to check first:

```sh
BASE_DIR="${1:-$PWD}"
```

If an argument is supplied:

```bash
dhruv /some/directory
```

that directory is used.

Otherwise:

```bash
$PWD
```

is used.

## `SEARCH_ROOT`

The root directory used for the fallback search:

```sh
SEARCH_ROOT="$HOME"
```

---

# Troubleshooting

## `tool set file is not found`

The launcher could not find:

```text
dhruv_tool_set.py
```

inside the specified/current directory or `$HOME`.

Check that the file exists:

```bash
find "$HOME" -name "dhruv_tool_set.py" 2>/dev/null
```

---

## The saved path is not being used

Check:

```bash
cat ~/.dhruv_tool_set_path
```

Then check whether that file still exists:

```bash
ls -l "$(cat ~/.dhruv_tool_set_path)"
```

If the path is invalid, remove the stored file:

```bash
rm ~/.dhruv_tool_set_path
```

and run the launcher again.

---

## `dhruv: command not found`

Check whether the launcher is in your PATH:

```bash
which dhruv
```

Check your PATH:

```bash
echo "$PATH"
```

Make sure:

```text
$HOME/.local/bin
```

is included.

---

## Permission denied

Make the launcher executable:

```bash
chmod +x ~/.local/bin/dhruv
```

---

## Python command not found

Check:

```bash
python3 --version
```

If Python 3 is not installed or is not available as `python3`, install/configure Python 3 for your system.

---

# Manual Reset

To completely reset the launcher's remembered location:

```bash
rm -f ~/.dhruv_tool_set_path
```

The launcher will behave as if it has never saved a path.

---

# Example Final Installation

A possible final setup:

```text
/home/dhruv/
│
├── .dhruv_tool_set_path
│
├── .local/
│   └── bin/
│       └── dhruv
│
└── dhruv-tool-set/
    ├── dhruv_tool_set.py
    └── README.md
```

Where:

```text
~/.local/bin/dhruv
```

is the global shell launcher, and:

```text
~/dhruv-tool-set/dhruv_tool_set.py
```

is the actual Python application.

The hidden file:

```text
~/.dhruv_tool_set_path
```

contains:

```text
/home/dhruv/dhruv-tool-set/dhruv_tool_set.py
```

---

# Summary

The launcher provides a simple way to run the Dhruv Tool Set from anywhere.

Its core behavior is:

```text
1. Check saved path
2. Check given/current directory
3. Search HOME
4. Ask before running a discovered copy
5. Ask whether to remember the selected path
6. Save the path if requested
7. Run the Python application
8. Reuse the saved path on future runs
```

The launcher itself does not store or modify the Python application. It only remembers **where the Python application is located**.

The remembered path is stored in:

```text
~/.dhruv_tool_set_path
```

and can be inspected or removed at any time.
