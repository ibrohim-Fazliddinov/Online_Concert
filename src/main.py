from fastapi import FastAPI

from src.auth.route import user_route

app = FastAPI()


app.include_router(user_route, prefix="",             # или "/api" — по вашему усмотрению
    tags=["auth"])




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app:app",     # или "main:app", или "src.auth_app:app"
        host="0.0.0.0",
        port=8000,
        reload=True,
    )