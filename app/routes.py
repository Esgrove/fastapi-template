from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

try:
    from app.models import API_NAME, DATABASE, Item, MessageResponse, VersionInfo
    from app.version import VERSION_NUMBER
except ModuleNotFoundError:
    from models import API_NAME, DATABASE, Item, MessageResponse, VersionInfo
    from version import VERSION_NUMBER

router = APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """
    Provide favicon.
    Not really needed but here to silence a warning.
    """
    return FileResponse("favicon.ico")


@router.get("/")
async def root_route() -> MessageResponse:
    """Show a simple info message."""
    return MessageResponse(message=f"{API_NAME} {VERSION_NUMBER}")


@router.get("/version/")
async def version_route() -> VersionInfo:
    """Return API version information."""
    return VersionInfo()


@router.get("/items/")
async def list_items(skip: int = 0, limit: int = 100) -> list[Item]:
    """
    Get a list of items.

    Optionally starting from `skip` index.
    Optionally up to `limit` items.
    """
    return list(DATABASE.values())[skip : skip + limit]


@router.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    """Return item for given id."""
    if item_id < 1000 or item_id > 9999:
        raise HTTPException(status_code=400, detail="Item ID must be be between 1000 and 9999")

    if item_id not in DATABASE:
        raise HTTPException(status_code=404, detail=f"Item ID {item_id} does not exist")

    return Item(name="test", item_id=item_id)


@router.post("/items/")
async def create_item(item: Item) -> Item:
    """Add item to database."""
    # Check if the item id already exists
    if item.item_id in DATABASE:
        raise HTTPException(status_code=409, detail="Item with this ID already exists")

    DATABASE[item.item_id] = item
    return item
