#!/usr/bin/env bash
set -eo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel || (cd "$(dirname "${BASH_SOURCE[0]}")" && pwd))
export REPO_ROOT

VERSION_FILE="$REPO_ROOT/app/version.py"

# Check platform
case "$(uname -s)" in
    "Darwin")
        BASH_PLATFORM="mac"
        ;;
    "MINGW"*)
        BASH_PLATFORM="windows"
        ;;
    *)
        BASH_PLATFORM="linux"
        ;;
esac
export BASH_PLATFORM

# Print a message in bold
print_bold() {
    printf "\e[1;49;37m%s\e[0m\n" "$1"
}

# Format text with green color
green() {
    printf "\e[1;49;32m%s\e[0m" "$1"
}

# Print a message with green color
print_green() {
    printf "\e[1;49;32m%s\e[0m\n" "$1"
}

# Print a message with cyan color
print_cyan() {
    printf "\e[1;49;36m%s\e[0m\n" "$1"
}

# Print a message with magenta color
print_magenta() {
    printf "\e[1;49;35m%s\e[0m\n" "$1"
}

# Format text with red color
red() {
    printf "\e[1;49;31m%s\e[0m" "$1"
}

# Print a message with red color
print_red() {
    printf "\e[1;49;31m%s\e[0m\n" "$1"
}

# Print a message with yellow color
print_yellow() {
    printf "\e[1;49;33m%s\e[0m\n" "$1"
}

# Print an error and exit the program
print_error_and_exit() {
    print_red "ERROR: $1"
    # use exit code if given as second argument, otherwise default to 1
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

# Read Python project version number from pyproject.toml
get_pyproject_version_number() {
    # note: `tomllib` requires Python 3.11+
    python3 -c 'with open("pyproject.toml", "rb") as f: \
                import tomllib; \
                project = tomllib.load(f); \
                print(project["tool"]["poetry"]["version"])'
}

# Set variables BUILD_TIME, GIT_HASH, and GIT_BRANCH
set_version_info() {
    BUILD_TIME=$(date +"%Y-%m-%d_%H%M")
    GIT_HASH=$(git -C "$REPO_ROOT" rev-parse --short HEAD)
    GIT_BRANCH=$(git -C "$REPO_ROOT" branch --show-current)
    export BUILD_TIME
    export GIT_HASH
    export GIT_BRANCH
}

# Update project version information file
update_version_information() {
    print_yellow "Updating version file: $VERSION_FILE"
    set_version_info
    VERSION_NUMBER="$(get_pyproject_version_number)"
    echo "DATE:    $BUILD_TIME"
    echo "BRANCH:  $GIT_BRANCH"
    echo "COMMIT:  $GIT_HASH"
    echo "VERSION: $VERSION_NUMBER"
    {
        echo '"""'
        echo 'Version information definitions'
        echo 'Akseli Lukkarila'
        echo '2019-2023'
        echo '"""'
        echo ""
        echo "# CREATED BY SCRIPT. DO NOT MODIFY MANUALLY."
        echo "BRANCH = \"$GIT_BRANCH\""
        echo "COMMIT = \"$GIT_HASH\""
        echo "DATE = \"$BUILD_TIME\""
        echo "VERSION_NUMBER = \"$VERSION_NUMBER\""
    } > "$VERSION_FILE"
}
