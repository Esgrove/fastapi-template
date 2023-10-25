import random

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from mangum import Mangum
from pydantic import BaseModel

from version import BRANCH, COMMIT, DATE, VERSION_NUMBER


app = FastAPI()


class Message(BaseModel):
    message: str


class Item(BaseModel):
    name: str
    item_id: int = random.randint(1000, 9999)

class VersionInfo(BaseModel):
    branch: str = BRANCH
    commit: str = COMMIT
    date: str = DATE
    version: str = VERSION_NUMBER


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse("favicon.ico")


@app.get("/")
async def root_route() -> Message:
    """Show hello message."""
    return Message(message=f"Hello World! FastAPI example {VERSION_NUMBER}")


@app.get("/status/")
async def status_route() -> VersionInfo:
    """Return status information."""
    return VersionInfo()


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    """Return item for given id."""
    return Item(name="test", item_id=item_id)


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 3) -> list[Item]:
    """
    Get a list of items.

    Optionally starting from `skip` index.
    Optionally up to `limit` items.
    """
    fake_items_db = [Item(name=name) for name in ("foo", "bar", "baz", "lorem", "ipsum", "dolor", "sit", "amet")]
    return fake_items_db[skip : skip + limit]


def start() -> None:
    """Helper for starting server with `poetry run start`."""
    uvicorn.run("app.main:app", reload=True)


# Mangum is an adapter for running ASGI applications in AWS Lambda
# https://mangum.io/
handler = Mangum(app, lifespan="off")
