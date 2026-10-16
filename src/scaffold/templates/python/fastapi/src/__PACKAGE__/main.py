import logging
import os

from fastapi import FastAPI

from __PACKAGE__.routes import router

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI(title="__PROJECT__")
app.include_router(router, prefix="/api/v1")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
