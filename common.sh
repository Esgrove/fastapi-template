#!/usr/bin/env bash
set -eo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel || (cd "$(dirname "${BASH_SOURCE[0]}")" && pwd))
export REPO_ROOT

# Check platform
case "$(uname -s)" in
    "Darwin")
        PLATFORM="mac"
        ;;
    "MINGW"*)
        PLATFORM="windows"
        ;;
    *)
        PLATFORM="linux"
        ;;
esac

# Print a message with green color
print_green() {
    printf "\e[1;49;32m%s\e[0m\n" "$1"
}

# Print a message with magenta color
print_magenta() {
    printf "\e[1;49;35m%s\e[0m\n" "$1"
}

# Print a message with red color
print_red() {
    printf "\e[1;49;31m%s\e[0m\n" "$1"
}

# Print a message with yellow color
print_yellow() {
    printf "\e[1;49;33m%s\e[0m\n" "$1"
}

print_error() {
    print_red "ERROR: $1"
}

print_warn() {
    print_yellow "WARNING: $1"
}

# Print an error message and exit the program
print_error_and_exit() {
    print_error "$1"
    # use exit code if given as argument, otherwise default to 1
    exit "${2:-1}"
}

# if DRYRUN or DRY_RUN has been set, only print commands instead of running them
run_command() {
    if [ "$DRY_RUN" = true ] || [ "$DRYRUN" = true ]; then
        echo "DRYRUN: $*"
    else
        echo "Running: $*"
        "$@"
    fi
}
