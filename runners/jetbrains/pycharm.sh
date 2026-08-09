#!/bin/sh
set -eu


# ============================================================
# Dhruv Tool Set Runner
#
# Copy this file when creating a new runner.
# Edit the required sections.
# ============================================================


# ============================================================
# Program name
# ============================================================

program_name="PyCharm"


# ============================================================
# Program command
# ============================================================

program_command="/home/dhruv/.local/share/JetBrains/Toolbox/apps/pycharm/bin/pycharm"


# ============================================================
# Variables
# ============================================================

# Add program-specific variables here.


# ============================================================
# Program pre-run setup commands
# ============================================================

# Add commands required before launching the program here.
#
# Example:
#
# . /path/to/settings.sh
#
# export SOME_VARIABLE="value"


# ============================================================
# User arguments
# ============================================================

# Optional argument.
# Press Enter without typing anything to launch without it.

printf '%s' "Enter argument (optional): "
read -r program_argument


# ============================================================
# Check program
# ============================================================

if [ ! -x "$program_command" ]; then
    printf '%s\n' "$program_name is not installed or not executable:"
    printf '%s\n' "$program_command"
    exit 1
fi


# ============================================================
# Launch program
# ============================================================

if [ -n "$program_argument" ]; then

    if ! "$program_command" "$program_argument"; then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

else

    if ! "$program_command"; then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

fi