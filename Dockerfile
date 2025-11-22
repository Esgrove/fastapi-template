# Dockerfile
# https://docs.docker.com/engine/reference/builder/

# Base Python image
FROM python:3.14-bullseye as python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.2 \
    PATH="/opt/poetry/bin:$PATH"

WORKDIR /fastapi_app

# Install Poetry
FROM python as poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | \
    POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry
RUN poetry --version

# Install dependencies
COPY . ./
RUN poetry install -vv --without dev,test

# Drop Poetry installation from final container,
# just copy runtime dependencies that were installed in `poetry`
FROM python as runtime
ENV PATH="/fastapi_app/.venv/bin:$PATH"
ENV FASTAPI_ENV=production
COPY --from=poetry /fastapi_app /fastapi_app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option `--proxy-headers`,
# this will tell Uvicorn to trust the headers sent by that proxy telling it that the application is running behind HTTPS.
# https://fastapi.tiangolo.com/deployment/docker/
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

HEALTHCHECK --interval=1m --timeout=3s \
    CMD curl -fs http://localhost/ || exit 1
