"""
FastAPI template and example.
Akseli Lukkarila
2019-2024
"""

import uvicorn
from fastapi import FastAPI
from mangum import Mangum

from app.admin import router as admin_router
from app.models import DATABASE, Item
from app.routes import router


def init_db():
    """Add some initial data to the database."""
    items = [Item(name=name) for name in ("foo", "bar", "baz", "lorem", "ipsum", "dolor", "sit", "amet")]
    for item in items:
        DATABASE[item.item_id] = item


def start() -> None:
    """Helper for starting server with `poetry run start`."""
    uvicorn.run("app.main:app", reload=True)


init_db()
app = FastAPI()
app.include_router(router)
app.include_router(admin_router, prefix="/admin")

# Mangum is an adapter for running ASGI applications in AWS Lambda
# https://mangum.io/
handler = Mangum(app, lifespan="off")
