from fastapi import APIRouter, HTTPException

try:
    from app.models import DATABASE, MessageResponse
except ModuleNotFoundError:
    from models import DATABASE, MessageResponse

router = APIRouter()


@router.delete("/items/{item_id}")
def delete_item(item_id: int) -> MessageResponse:
    """Delete an item from the database."""
    if item_id in DATABASE:
        message = f"Deleted item: {DATABASE[item_id]}"
        del DATABASE[item_id]
        return MessageResponse(message=message)

    raise HTTPException(status_code=404, detail="Item ID does not exist")


@router.delete("/clear_items/")
def delete_all_item() -> MessageResponse:
    """Delete an item from the database."""
    num_items = len(DATABASE)
    message = f"Deleted all {num_items} items"
    DATABASE.clear()
    return MessageResponse(message=message)
