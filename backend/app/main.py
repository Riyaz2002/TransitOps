from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="TransitOps API", version="0.1.0")
app.include_router(router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
