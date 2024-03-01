from fastapi import APIRouter, status
from fastapi.responses import FileResponse, JSONResponse

try:
    from app.models import API_NAME, DATABASE, Item, MessageResponse, ServerError, VersionInfo, message_response
    from app.version import VERSION_NUMBER
except ModuleNotFoundError:
    from models import API_NAME, DATABASE, Item, MessageResponse, ServerError, VersionInfo, message_response
    from version import VERSION_NUMBER

router = APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """
    Provide favicon.
    Not really needed but here to silence a warning.
    """
    return FileResponse("../favicon.ico")


@router.get("/")
async def root_route() -> MessageResponse:
    """Show a simple info message."""
    return MessageResponse.new(f"{API_NAME} {VERSION_NUMBER}")


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


@router.get("/keys/")
async def list_keys(skip: int = 0, limit: int = 100) -> list[int]:
    """
    Get a list of keys (item IDs).

    Optionally starting from `skip` index.
    Optionally up to `limit` items.
    """
    return list(DATABASE.keys())[skip : skip + limit]


@router.get(
    "/items/{item_id}",
    response_model=Item | MessageResponse,
    responses={
        400: {"model": MessageResponse, "description": "Invalid item ID"},
        404: {"model": MessageResponse, "description": "Item not found"},
    },
)
async def read_item(item_id: int):
    """Return item for given id."""
    if item_id < 1000 or item_id > 9999:
        return message_response(400, "Item ID must be be between 1000 and 9999")

    if item_id not in DATABASE:
        return message_response(404, f"Item ID does not exist: {item_id}")

    return DATABASE.get(item_id)


@router.post(
    "/items/",
    status_code=status.HTTP_201_CREATED,
    response_model=Item | MessageResponse,
    responses={409: {"model": MessageResponse, "description": "Item already exists"}},
)
async def create_item(item: Item):
    """Add item to database."""
    # Check if the item id already exists
    if item.item_id in DATABASE:
        # Using `message_response` would simplify creating the JSONResponse,
        # but leaving this here to show it directly.
        return JSONResponse(
            status_code=409,
            content=MessageResponse(
                message=f"Item with this ID already exists: {DATABASE.get(item.item_id)}"
            ).model_dump(),
        )

    DATABASE[item.item_id] = item
    return item


@router.post(
    "/items/bulk/",
    status_code=status.HTTP_201_CREATED,
    response_model=list[Item],
    responses={409: {"model": MessageResponse, "description": "One or more items already exist"}},
)
async def create_items(items: list[Item]):
    """Add one or more items to the database."""
    conflict_items = []
    for item in items:
        if item.item_id in DATABASE:
            conflict_items.append(item)
        else:
            DATABASE[item.item_id] = item
    if conflict_items:
        return message_response(409, f"Items already exist: {','.join(i.item_id for i in conflict_items)}")

    return items


@router.get("/exception/")
async def test_exception() -> float:
    """Route for testing custom exception."""
    try:
        num_items = len(DATABASE)
        divider = 0
        result = num_items / divider
        return result
    except ZeroDivisionError:
        raise ServerError("Division by zero error")
