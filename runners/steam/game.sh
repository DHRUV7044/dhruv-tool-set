#!/bin/sh
set -eu


# ============================================================
# Program name
# ============================================================

program_name="${DTS_NAME:-Steam Game}"


# ============================================================
# Program command
# ============================================================

program_command="steam"


# ============================================================
# Variables
# ============================================================

steam_app_id="${DTS_APP_ID:-}"


# ============================================================
# Check App ID
# ============================================================

if [ -z "$steam_app_id" ]; then
    printf '%s\n' "Steam App ID was not provided."
    exit 1
fi


# ============================================================
# Check Steam
# ============================================================

if ! command -v "$program_command" >/dev/null 2>&1; then
    printf '%s\n' "Steam is not installed or not available in PATH."
    exit 1
fi


# ============================================================
# Launch game
# ============================================================

if ! "$program_command" -applaunch "$steam_app_id"; then
    printf '%s\n' "Failed to start $program_name."
    exit 1
fi