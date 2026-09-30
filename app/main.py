"""Точка входа (аналог Program.cs).

Запуск:  uvicorn app.main:app --reload --port 5145
Swagger: http://localhost:5145/swagger
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import settings
from app.database import engine
from app.routers import filter_data, last_ten_values, table_actions, upload_and_read

logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="TimescaleApi", version="v1", docs_url="/swagger", redoc_url=None, lifespan=lifespan)

app.include_router(filter_data.router)
app.include_router(last_ten_values.router)
app.include_router(table_actions.router)
app.include_router(upload_and_read.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/swagger")
