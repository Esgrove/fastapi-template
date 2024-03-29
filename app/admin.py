from fastapi import APIRouter

try:
    from app.models import DATABASE, MessageResponse, message_response
except ModuleNotFoundError:
    from models import DATABASE, MessageResponse, message_response

router = APIRouter()


@router.delete(
    "/items/{item_id}",
    response_model=MessageResponse,
    responses={404: {"model": MessageResponse, "description": "Item does not exist"}},
)
def delete_item(item_id: int):
    """Delete an item from the database."""
    if item_id in DATABASE:
        message = f"Deleted item: {DATABASE[item_id]}"
        del DATABASE[item_id]
        return MessageResponse.new(message)

    return message_response(404, "Item ID does not exist")


@router.delete(
    "/items/name/{name}",
    response_model=MessageResponse,
    responses={404: {"model": MessageResponse, "description": "Item does not exist"}},
)
def delete_item_by_name(name: str):
    """Delete an item from the database by item name."""
    for item_id, item in DATABASE.items():
        if item.name == name:
            message = f"Deleted item: {item}"
            del DATABASE[item_id]
            return MessageResponse.new(message)

    return message_response(404, "Item name does not exist")


@router.delete("/clear_items/")
def delete_all_items() -> MessageResponse:
    """Delete an item from the database."""
    num_items = len(DATABASE)
    message = f"Deleted all {num_items} items"
    DATABASE.clear()
    return MessageResponse.new(message)
