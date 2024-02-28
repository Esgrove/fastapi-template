import random
from typing import Self

from fastapi.responses import JSONResponse
from pydantic import BaseModel

try:
    from app.version import BRANCH, COMMIT, DATE, VERSION_NUMBER
except ModuleNotFoundError:
    from version import BRANCH, COMMIT, DATE, VERSION_NUMBER

API_NAME = "FastAPI example"


class MessageResponse(BaseModel):
    """Simple return message."""

    message: str

    @classmethod
    def new(cls, message: str) -> Self:
        """
        A bit of Rust inspiration in Python:
        Factory method to create a `MessageResponse`,
        without needing to specify the `message` parameter name.
        So instead of `MessageResponse(message=message)`,
        one can use `MessageResponse.new(message)`
        """
        return cls(message=message)


class ApiError(Exception):
    def __init__(self, name: str):
        self.name = name


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


def message_response(status_code: int, message: str) -> JSONResponse:
    """Helper function to create a JSONResponse with a MessageResponse model."""
    response_content = MessageResponse(message=message).dict()
    return JSONResponse(status_code=status_code, content=response_content)
