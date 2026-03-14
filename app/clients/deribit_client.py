import asyncio
import aiohttp
from app.crud import ticker as ticker_service
from app.db.session import get_db


class DeribitClient:
    BASE_URL = "https://test.deribit.com/api/v2/public"

    def __init__(self):
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession()

    async def get_index_price(self, index_name: str) -> None:
        url = f"{self.BASE_URL}/get_index_price"
        async with self.session.get(url, params={"index_name": index_name}) as resp:
            data = await resp.json()
            price = data["result"]["index_price"]
            self.save_ticker(index_name, price)
            return price

    def save_ticker(self, name: str, price: float) -> None:
        gen = get_db()
        db = next(gen)
        try:
            ticker_service.create_ticker(db, name, price)
        finally:
            gen.close()

    async def close(self):
        await self.session.close()


async def main():
    client = DeribitClient()
    await client.start()

    btc = await client.get_index_price("btc_usd")
    eth = await client.get_index_price("eth_usd")
    print("BTC:", btc, "ETH:", eth)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
