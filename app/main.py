from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1.prices import router as price_router

app = FastAPI(
    title="Deribit Price Tracker",
    description="API for tracking index prices from Deribit exchange.",
    version="1.0.0",
)

app.include_router(price_router, prefix="/api/v1")

init_db()
