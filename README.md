# FastAPI template

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[FastAPI](https://github.com/tiangolo/fastapi) REST API project template and example.
Uses [Poetry](https://github.com/python-poetry/poetry) for project and dependency management.

## Dependencies

Requires:

- Python 3.11+
- Scripts use [jq](https://jqlang.github.io/jq/) and Docker but not strictly needed

Install Python dependencies:

```shell
poetry install
```

Update dependencies:

```shell
poetry update
```

## Quick start

Use the provided shell scripts to easily run unit tests and the API locally with Docker with the scripts:

```shell
./test.sh
./run.sh
```

## Tests

Tests use pytest.

```shell
poetry run pytest -v
```

Run tests with coverage report:

```shell
poetry run pytest -v --cov=app tests/
```

## Running server locally

Start a development server locally with a shortcut:

```shell
poetry run start
# with optional args
poetry run start --port 3000 --log debug
```

Or full command with all available uvicorn args:

```shell
poetry run uvicorn app.main:app --reload --host localhost --port 8000
```

### Using Docker

Build Docker image and run container with the script:

```shell
./run.sh
```

Or manually:

```shell
docker build -t runtime .
docker run -d --name fastapi -p 80:80 runtime
```

### Test API locally

With script with nice formatting:

```shell
./test-routes.sh
```

Manually:

```shell
curl -s http://127.0.0.1:8000/ | jq .
curl -s http://127.0.0.1:8000/items/1234 | jq .
curl -s http://127.0.0.1:8000/items/ | jq .
curl -s http://127.0.0.1:8000/items/?limit=8 | jq .
```

### Interactive API docs

FastAPI automatically generates an OpenAPI schema for the API,
which is used to render the documentation:

- [Swagger UI](https://github.com/swagger-api/swagger-ui) documentation is available at <http://127.0.0.1:8000/docs>
- [ReDoc](https://github.com/Redocly/redoc) documentation is available at <http://127.0.0.1:8000/redoc>

**Note:** The server needs to be running for these to work. With Docker, you can drop the port number :wink:

## Code formatting and linting

Code formatting and linting with [ruff](https://github.com/charliermarsh/ruff).
Import sorting with [isort](https://github.com/PyCQA/isort).

These are configured with a custom line length limit of 120.
The configs can be found in [pyproject.toml](./pyproject.toml).

Usage:

```shell
isort .
ruff format .
ruff --fix .
```

Using with [pre-commit](https://pre-commit.com/):

```shell
# setup to be run automatically on git commit
pre-commit install

# run manually
pre-commit run --all-files
```

## TODO

- Setup [coveralls](https://coveralls.io/)
- Better API usage examples
- Improve test cases
