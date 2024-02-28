import random

from pydantic import BaseModel

from app.version import BRANCH, COMMIT, DATE, VERSION_NUMBER

API_NAME = "FastAPI example"


class MessageResponse(BaseModel):
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
