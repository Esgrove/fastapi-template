#!/usr/bin/env bash
set -eo pipefail

# Run API locally with Docker

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$DIR/common.sh"

cd "$REPO_ROOT" > /dev/null

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

print_magenta "Testing routes..."
echo "http://127.0.0.1"
curl -s http://127.0.0.1 | jq .

echo "http://127.0.0.1/version/"
curl -s http://127.0.0.1/version/ | jq .

echo "http://127.0.0.1/items/123"
curl -s http://127.0.0.1/items/1234 | jq .

echo "http://127.0.0.1/items/"
curl -s http://127.0.0.1/items/ | jq .

echo "http://127.0.0.1/items/?limit=8"
curl -s http://127.0.0.1/items/?limit=8 | jq .

if [ "$PLATFORM" = mac ]; then
    print_magenta "Opening API docs..."
    run_command open http://127.0.0.1/redoc
fi
