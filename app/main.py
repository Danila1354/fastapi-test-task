from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1.prices import router as price_router

app = FastAPI()

app.include_router(price_router)

init_db()
