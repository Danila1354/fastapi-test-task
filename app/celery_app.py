from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.broker_url,
    backend="rpc://",
    include=["app.tasks.fetch_prices"],
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.fetch_prices.fetch_prices",
        "schedule": 60.0,
    },
}

celery_app.conf.timezone = "UTC"
