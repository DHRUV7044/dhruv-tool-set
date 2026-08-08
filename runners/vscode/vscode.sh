#!/bin/sh
set -eu

# ==============================
# Program name
# ==============================

program_name="Visual Studio Code"
program_command="code"


# ==============================
# Variables
# ==============================


# ==============================
# Program pre-run setup commands
# ==============================


# ==============================
# User arguments
# ==============================

printf '%s' "Enter path to open (leave empty for none): "
read -r target


# ==============================
# Check program
# ==============================

if ! command -v "$program_command" >/dev/null 2>&1; then
    printf '%s\n' "$program_name is not installed or not available in PATH."
    exit 1
fi


# ==============================
# Launch program
# ==============================

if [ -n "$target" ]; then
    if ! "$program_command" "$target"; then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi
else
    if ! "$program_command"; then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi
fi