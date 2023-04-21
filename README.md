# FastAPI template

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[FastAPI](https://github.com/tiangolo/fastapi) project template.

## Dependencies

Requires Python 3.11+

Dependencies are managed by [Poetry](https://python-poetry.org/docs/).

Install dependencies:

```shell
poetry install
```

Update dependencies:

```shell
poetry update
```

Adding dependencies:

```shell
poetry add fastapi uvicorn
poetry add pytest --group test
poetry add black pyupgrade ruff --group dev
```

## Tests

Tests use pytest.

```shell
poetry run pytest
```

Run tests with coverage report:

```shell
poetry run pytest --cov=app tests/
```

## Running locally

Start a development server locally:

```shell
peotry run start
```

Or:

```shell
poetry run uvicorn app.main:app --reload --host localhost --port 8000
```

### Using Docker

```shell
docker build -t runtime .
docker run -d --name fastapi -p 80:80 runtime
```

### Interactive API docs

FastAPI automatically generates an OpenAPI schema for the API,
which is used to render the documentation:

- [Swagger UI](https://github.com/swagger-api/swagger-ui) documentation is available at <http://127.0.0.1:8000/docs>
- [ReDoc](https://github.com/Redocly/redoc) documentation is available at <http://127.0.0.1:8000/redoc>

**Note:** The server needs to be running for these to work. With Docker, you can drop the port number :wink:

## Code formatting and linting

Code formatting with [Black](https://github.com/psf/black).
Import sorting with [isort](https://github.com/PyCQA/isort).
Linting with [ruff](https://github.com/charliermarsh/ruff).

These are configured with a custom line length limit of 120.
The configs can be found in [pyproject.toml](./pyproject.toml).

Usage:

```shell
black .
isort .
ruff --fix .
```

These can also be integrated to IDEs / editors or run as a pre-commit hook.
See the documentation for Black [here](https://black.readthedocs.io/en/stable/integrations/editors.html).
Visual Studio Code has built-in support for
[Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
and
[isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
through official plugins.
There is also a [Ruff extension](https://github.com/charliermarsh/ruff-vscode) for VS Code.

Using with [pre-commit](https://pre-commit.com/):

```shell
# setup to be run automatically on git commit
pre-commit install

# run manually
pre-commit run --all-files
```

## TODO

- Setup [coveralls](https://coveralls.io/)
