import asyncio
from app.celery_app import celery_app
from app.clients.deribit_client import DeribitClient


@celery_app.task
def fetch_prices():
    asyncio.run(run())


async def run():
    client = DeribitClient()
    await client.start()

    await asyncio.gather(
        client.get_index_price("btc_usd"), client.get_index_price("eth_usd")
    )

    await client.close()
