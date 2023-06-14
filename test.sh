#!/usr/bin/env bash
set -eo pipefail

# Run Python tests

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$DIR/common.sh"

cd "$REPO_ROOT" > /dev/null
print_magenta "Running tests..."
poetry run pytest --cov=app tests/ -v
