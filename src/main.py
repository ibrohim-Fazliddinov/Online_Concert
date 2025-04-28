from fastapi import FastAPI
from contextlib import  asynccontextmanager
from src.auth.utils import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Init tables """
    print("Create")
    create_tables()
    yield # sep point

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def hello_world():
    return {"message": "HELLO WORLD"}