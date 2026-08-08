#!/bin/sh
set -eu

# ==============================
# Program name
# ==============================

program_name="VLC"
program_command="vlc"


# ==============================
# Variables
# ==============================


# ==============================
# Program pre-run setup commands
# ==============================


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

if ! "$program_command"; then
    printf '%s\n' "Failed to start $program_name."
    exit 1
fi