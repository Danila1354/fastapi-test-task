import asyncio
from app.celery_app import celery_app
from app.clients.deribit_client import DeribitClient
from app.db.session import get_db_context
from app.services.ticker import TickerService


@celery_app.task
def fetch_prices():
    asyncio.run(_fetch_and_save())


async def _fetch_and_save():
    async with DeribitClient() as client:
        btc_price, eth_price = await asyncio.gather(
            client.get_index_price("btc_usd"),
            client.get_index_price("eth_usd"),
        )

    with get_db_context() as db:
        service = TickerService(db)
        service.create_ticker("btc_usd", btc_price)
        service.create_ticker("eth_usd", eth_price)
