import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/")
async def root_route():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return fake_items_db[skip : skip + limit]


def start():
    """Helper for starting server with `poetry run start`."""
    uvicorn.run("app.main:app", reload=True)


handler = Mangum(app, lifespan="off")
