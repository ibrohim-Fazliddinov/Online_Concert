from fastapi import FastAPI
from contextlib import  asynccontextmanager

from src.common.model import Base

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "HELLO WORLD"}