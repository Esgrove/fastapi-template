"""
FastAPI template and example.
Akseli Lukkarila
2019-2023
"""

import random

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from mangum import Mangum
from pydantic import BaseModel

from app.version import BRANCH, COMMIT, DATE, VERSION_NUMBER

app = FastAPI()
API_NAME = "FastAPI example"


class Message(BaseModel):
    """Simple return message."""

    message: str


class Item(BaseModel):
    """Basic item with name and id."""

    name: str
    item_id: int

    # Assign random id if it was not specified
    def __init__(self, **data):
        if "item_id" not in data:
            data["item_id"] = random.randint(1000, 9999)

        super().__init__(**data)


class VersionInfo(BaseModel):
    """Version information message."""

    name: str = API_NAME
    branch: str = BRANCH
    commit: str = COMMIT
    date: str = DATE
    version: str = VERSION_NUMBER


# Simulated database
DATABASE: dict[int, Item] = {}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """
    Provide favicon.
    Not really needed but here to silence a warning.
    """
    return FileResponse("favicon.ico")


@app.get("/")
async def root_route() -> Message:
    """Show hello message."""
    return Message(message=f"{API_NAME} {VERSION_NUMBER}")


@app.get("/version/")
async def version_route() -> VersionInfo:
    """Return API version information."""
    return VersionInfo()


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100) -> list[Item]:
    """
    Get a list of items.

    Optionally starting from `skip` index.
    Optionally up to `limit` items.
    """
    return list(DATABASE.values())[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    """Return item for given id."""
    if item_id < 1000 or item_id > 9999:
        raise HTTPException(status_code=400, detail="Item ID must be be between 1000 and 9999")

    if item_id not in DATABASE:
        raise HTTPException(status_code=404, detail=f"Item ID {item_id} does not exist")

    return Item(name="test", item_id=item_id)


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """Add item to database."""
    # Check if the item id already exists
    if item.item_id in DATABASE:
        raise HTTPException(status_code=409, detail="Item with this ID already exists")

    DATABASE[item.item_id] = item
    return item


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> Message:
    """Delete an item from the database."""
    global DATABASE
    if item_id in DATABASE:
        message = f"Deleted item: {DATABASE[item_id]}"
        del DATABASE[item_id]
        return Message(message=message)

    raise HTTPException(status_code=404, detail="Item ID does not exist")


def init_db():
    """Add some initial data to the database."""
    global DATABASE
    items = [Item(name=name) for name in ("foo", "bar", "baz", "lorem", "ipsum", "dolor", "sit", "amet")]
    for item in items:
        DATABASE[item.item_id] = item


def start() -> None:
    """Helper for starting server with `poetry run start`."""
    uvicorn.run("app.main:app", reload=True)


init_db()

# Mangum is an adapter for running ASGI applications in AWS Lambda
# https://mangum.io/
handler = Mangum(app, lifespan="off")
