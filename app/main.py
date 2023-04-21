import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def main_route():
    return {"message": "Hello World"}


def start():
    """Helper for starting server with `poetry run start`."""
    uvicorn.run("app.main:app", reload=True)


handler = Mangum(app, lifespan="off")
