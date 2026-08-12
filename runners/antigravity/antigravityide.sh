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

program_name="Antigravity IDE"


# ============================================================
# Program command
# ============================================================

program_command="./antigravity-ide"


# ============================================================
# Variables
# ============================================================

# Add program-specific variables here.

path_to_runnable_file="/home/dhruv/antigravity/Antigravity IDE"


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

cd "$path_to_runnable_file" || {
    printf '%s\n' "Failed to change directory to $path_to_runnable_file."
    exit 1
}


# ============================================================
# User arguments
# ============================================================

# Optional argument.
# Press Enter without typing anything to launch without it.

printf '%s' "Enter argument (optional) (--no-sandbox  if this script does not have root access which it do not have by default): "
read -r program_argument


# ============================================================
# Check program
# ============================================================

if ! command -v "$program_command" >/dev/null 2>&1; then
    printf '%s\n' "$program_name is not installed or not available in PATH."
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