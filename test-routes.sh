#!/bin/bash
set -eo pipefail

# Import common functions
DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=../common.sh
source "$DIR/common.sh"

USAGE="Usage: $0 [OPTIONS]

Test API routes.
Port number can be set with env variable as well: PORT=3000 $0

OPTIONS: All options are optional
    -h | --help
        Display these instructions.

    -p | --port [NUMBER]
        Specify port number to use. Default is 8000.

    -v | --verbose
        Display commands being executed."

while [ $# -gt 0 ]; do
    case "$1" in
        -h | --help)
            print_usage_and_exit
            ;;
        -p | --port)
            PORT=$2
            shift
            ;;
        -v | --verbose)
            set -x
            ;;
    esac
    shift
done

PORT=${PORT:-8000}

get() {
    local url="$1"
    print_magenta "GET: $1"
    response=$(curl -s -w "%{http_code}" -o response.json "$url")
    print_response "$response"
}

post() {
    local url="$1"
    local data="$2"
    print_cyan "POST: $1 $2"
    response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" -w "%{http_code}" -o response.json "$url")
    print_response "$response"
}

delete() {
    local url="$1"
    print_red "DELETE: $1"
    response=$(curl -s -X DELETE -w "%{http_code}" -o response.json "$url")
    print_response "$response"
}

print_response() {
    local response="$1"
    if echo "$response" | grep -q '^2'; then
        echo "Status code: $(green "$response")"
    elif echo "$response" | grep -q '^4'; then
        echo "Status code: $(red "$response")"
    else
        echo "Status code: $response"
    fi
    output=$(jq --color-output < response.json)
    if [ "$(echo "$output" | wc -l)" -gt 1 ]; then
        echo "Response:"
        echo "$output"
    else
        echo "Response: $output"
    fi
    rm response.json
}

if ! curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT" | grep -q '^2'; then
    print_error_and_exit "Failed to call API, is it running?"
fi

get "http://127.0.0.1:$PORT"
get "http://127.0.0.1:$PORT/version"
get "http://127.0.0.1:$PORT/items/1234"
get "http://127.0.0.1:$PORT/items/"
get "http://127.0.0.1:$PORT/user?username=esgrove"
get "http://127.0.0.1:$PORT/items/?skip=3&limit=5"
