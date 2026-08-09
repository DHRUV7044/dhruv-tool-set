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

program_name="WhatsApp"


# ============================================================
# Program command
# ============================================================

program_command="/opt/google/chrome/google-chrome"


# ============================================================
# Program arguments
# ============================================================

program_profile="Profile 1"
program_app_id="hnpfjngllnobngcgfapefoaidbinmjnm"


# ============================================================
# Variables
# ============================================================

# Add program-specific variables here.


# ============================================================
# Program pre-run setup commands
# ============================================================

# Add commands required before launching the program here.

cd "$HOME/.local/share/applications"


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
    printf '%s\n' "$program_name is not installed or not executable."
    exit 1
fi


# ============================================================
# Launch program
# ============================================================

if [ -n "$program_argument" ]; then

    if ! "$program_command" \
        --profile-directory="$program_profile" \
        --app-id="$program_app_id" \
        "$program_argument"
    then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

else

    if ! "$program_command" \
        --profile-directory="$program_profile" \
        --app-id="$program_app_id"
    then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

fi