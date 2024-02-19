#!/usr/bin/env bash
set -eo pipefail

# Run API locally with Docker

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$DIR/common.sh"

cd "$REPO_ROOT"

if ! docker info > /dev/null 2>&1; then
    if [ "$BASH_PLATFORM" = mac ]; then
        print_yellow "Docker does not seem to be running. Starting Docker..."
        open -a Docker.app
        sleep 10
        if ! docker info > /dev/null 2>&1; then
            print_error_and_exit "Timed out waiting for Docker to start..."
        fi
    else
        print_error_and_exit "Docker does not seem to be running. Start Docker first..."
    fi
fi

if [ -z "$(docker ps -q --filter "name=fastapi")" ]; then
    print_magenta "Building Docker image..."
    update_version_information
    docker build -t runtime .

    print_magenta "Running API..."
    docker run -d --name fastapi -p 80:80 runtime

    echo "Waiting for container to start..."
    while ! curl -fs http://127.0.0.1 > /dev/null; do
        sleep 1
    done
    print_green "API is running"
else
    echo "Docker image is running, skipping build..."
fi

# Helper function to call api route
test_route() {
    echo "Route: $*"
    curl -s "$@" | jq .
}

print_magenta "Testing routes..."
test_route "http://127.0.0.1"
test_route "http://127.0.0.1/version/"
test_route "http://127.0.0.1/items/1234"
test_route "http://127.0.0.1/items/"
test_route "http://127.0.0.1/items/?skip=3&limit=5"

if [ "$BASH_PLATFORM" = mac ]; then
    print_magenta "Opening API docs..."
    open http://127.0.0.1/redoc
fi
