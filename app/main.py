"""
FastAPI REST example.
Akseli Lukkarila
2019-2024
"""

import traceback

import click
import uvicorn

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

try:
    from app.admin import router as admin_router
    from app.models import DATABASE, Item, ServerError
    from app.routes import router
except ModuleNotFoundError:
    from admin import router as admin_router
    from models import DATABASE, Item, ServerError
    from routes import router


def init_db():
    """Add some initial data to the database."""
    items = [Item(name=name) for name in ("foo", "bar", "baz", "lorem", "ipsum", "dolor", "sit", "amet")]
    for item in items:
        DATABASE[item.item_id] = item


@click.command()
@click.option("-h", "--host", default="127.0.0.1", help="Host IP to run the server on")
@click.option("-p", "--port", default=8000, help="Port number to use")
@click.option(
    "-l",
    "--log",
    "log_level",
    default="info",
    help="Set logging level",
    type=click.Choice(["trace", "debug", "info", "warning", "error", "critical"], case_sensitive=False),
)
def start(host: str, port: int, log_level: str):
    """FastAPI example."""

    # Helper for starting server with `poetry run start`
    uvicorn.run("app.main:app", host=host, port=port, log_level=log_level, reload=True)


init_db()
app = FastAPI()
app.include_router(router)
app.include_router(admin_router, prefix="/admin")


# Define an exception handler for custom exception
@app.exception_handler(ServerError)
async def server_error_exception_handler(request, exc):
    stack_trace = traceback.format_exc(limit=1)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Server error: {exc.name}", "stack_trace": stack_trace},
    )


# Mangum is an adapter for running ASGI applications in AWS Lambda
# https://mangum.io/
# handler = Mangum(app, lifespan="off")


if __name__ == "__main__":
    start()
