from fastapi import FastAPI

app = FastAPI()








if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app:app",     # или "main:app", или "src.auth_app:app"
        host="0.0.0.0",
        port=8000,
        reload=True,
    )