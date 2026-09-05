from fastapi import FastAPI
from api import router
from config import settings

app = FastAPI(title=settings.app_name)
app.include_router(router, prefix="/support", tags=["support"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )