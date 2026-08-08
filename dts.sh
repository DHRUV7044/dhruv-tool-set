#!/bin/sh

set -eu

TARGET_FILE="dhruv_tool_set.py"
STORE_FILE="$HOME/.dhruv_tool_set_path"
BASE_DIR="${1:-$PWD}"
SEARCH_ROOT="$HOME"

# ------------------------------------------------------------
# Validate given directory
# ------------------------------------------------------------

if [ ! -d "$BASE_DIR" ]; then
    echo "Given directory does not exist: $BASE_DIR"
    exit 1
fi

BASE_DIR="$(cd "$BASE_DIR" && pwd)"
DIRECT_MATCH="$BASE_DIR/$TARGET_FILE"

# ------------------------------------------------------------
# 1. Check previously stored path FIRST
# ------------------------------------------------------------

if [ -f "$STORE_FILE" ]; then

    STORED_PATH="$(cat "$STORE_FILE")"

    if [ -f "$STORED_PATH" ]; then
        exec python3 "$STORED_PATH"
    else
        echo "Stored path is no longer valid."
        rm -f "$STORE_FILE"
    fi
fi

# ------------------------------------------------------------
# 2. Check given/current directory
# ------------------------------------------------------------

if [ -f "$DIRECT_MATCH" ]; then

    echo
    echo "Found tool set file:"
    echo "  $DIRECT_MATCH"
    echo

    printf "Run this file? [Y/n]: "
    read -r RUN_ANSWER

    case "$RUN_ANSWER" in
        n|N|no|NO|No)
            echo "Not running."
            exit 0
            ;;
    esac

    echo
    printf "Store this path for future use? [Y/n]: "
    read -r STORE_ANSWER

    case "$STORE_ANSWER" in
        n|N|no|NO|No)
            echo "Path was not stored."
            ;;

        *)
            printf '%s\n' "$DIRECT_MATCH" > "$STORE_FILE"
            echo "Path stored in:"
            echo "  $STORE_FILE"
            ;;
    esac

    echo
    echo "Starting tool set..."
    exec python3 "$DIRECT_MATCH"
fi

# ------------------------------------------------------------
# 3. Search HOME for other copies
# ------------------------------------------------------------

MATCH_LIST="${TMPDIR:-/tmp}/dhruv_tool_set_matches_$$.txt"

cleanup() {
    rm -f "$MATCH_LIST"
}

trap cleanup EXIT INT TERM

find "$SEARCH_ROOT" \
    -type f \
    -name "$TARGET_FILE" \
    2>/dev/null |
    sort > "$MATCH_LIST"

# ------------------------------------------------------------
# 4. Ask user about found files
# ------------------------------------------------------------

FOUND=0

while IFS= read -r FILE_PATH
do

    if [ "$FILE_PATH" = "$DIRECT_MATCH" ]; then
        continue
    fi

    FOUND=1

    echo
    echo "Found tool set file:"
    echo "  $FILE_PATH"
    echo

    printf "Run this file? [Y/n]: "
    read -r RUN_ANSWER

    case "$RUN_ANSWER" in
        n|N|no|NO|No)
            echo "Skipped."
            continue
            ;;
    esac

    echo
    printf "Store this path for future use? [Y/n]: "
    read -r STORE_ANSWER

    case "$STORE_ANSWER" in
        n|N|no|NO|No)
            echo "Path was not stored."
            ;;

        *)
            printf '%s\n' "$FILE_PATH" > "$STORE_FILE"
            echo "Path stored in:"
            echo "  $STORE_FILE"
            ;;
    esac

    echo
    echo "Starting tool set..."
    exec python3 "$FILE_PATH"

done < "$MATCH_LIST"

# ------------------------------------------------------------
# 5. Nothing found
# ------------------------------------------------------------

if [ "$FOUND" -eq 0 ]; then
    echo "tool set file is not found"
else
    echo "No file was selected to run."
fi

exit 0