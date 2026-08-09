#!/bin/sh
set -eu


# ============================================================
# Dhruv Tool Set Runner
# ============================================================


# ============================================================
# Program name
# ============================================================

program_name="Firefox"


# ============================================================
# Program command
# ============================================================

program_command="firefox"


# ============================================================
# Variables
# ============================================================


# ============================================================
# Program pre-run setup commands
# ============================================================


# ============================================================
# Check program
# ============================================================

if ! command -v "$program_command" >/dev/null 2>&1; then
    printf '%s\n' "$program_name is not installed or not available in PATH."
    exit 1
fi


# ============================================================
# User arguments
# ============================================================

printf '%s' "Enter argument (optional, '&' to run detached): "
read -r program_argument


# ============================================================
# Launch program
# ============================================================

if [ "$program_argument" = "&" ]; then

    if ! "$program_command" >/dev/null 2>&1 </dev/null & then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

elif [ -n "$program_argument" ]; then

    if ! "$program_command" "$program_argument"; then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

else

    if ! "$program_command"; then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

else