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

program_name="Vivado 2024.2"


# ============================================================
# Program command
# ============================================================

program_command="vivado"


# ============================================================
# Variables
# ============================================================

vivado_setting_runner_path="/home/dhruv/vivado/tool/vivado_2024.2/Vivado/2024.2/settings64.sh"

log_file_path="$HOME/vivado_log_report/2024.2"


# ============================================================
# Program pre-run setup
# ============================================================

if [ ! -f "$vivado_setting_runner_path" ]; then
    printf '%s\n' "Vivado settings file not found:"
    printf '%s\n' "$vivado_setting_runner_path"
    exit 1
fi

if [ ! -d "$log_file_path" ]; then
    printf '%s\n' "Log directory not found:"
    printf '%s\n' "$log_file_path"
    exit 1
fi


# ============================================================
# User arguments
# ============================================================

printf '%s' "Enter argument (optional, '&' to run in background): "
read -r program_argument


# ============================================================
# Launch program
# ============================================================

if [ "$program_argument" = "&" ]; then

    if ! bash -c '
        set -e

        . "$1"

        cd "$2"

        nohup "$3" >/dev/null 2>&1 </dev/null &
    ' _ \
        "$vivado_setting_runner_path" \
        "$log_file_path" \
        "$program_command"
    then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

    printf '%s\n' "$program_name started in background."

elif [ -n "$program_argument" ]; then

    if ! bash -c '
        set -e

        . "$1"

        cd "$2"

        exec "$3" "$4"
    ' _ \
        "$vivado_setting_runner_path" \
        "$log_file_path" \
        "$program_command" \
        "$program_argument"
    then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

else

    if ! bash -c '
        set -e

        . "$1"

        cd "$2"

        exec "$3"
    ' _ \
        "$vivado_setting_runner_path" \
        "$log_file_path" \
        "$program_command"
    then
        printf '%s\n' "Failed to start $program_name."
        exit 1
    fi

fi