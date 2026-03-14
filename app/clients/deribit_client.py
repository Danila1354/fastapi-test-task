import asyncio
import aiohttp


class DeribitClient:
    BASE_URL = "https://test.deribit.com/api/v2/public"

    def __init__(self) -> None:
        self.session = None

    async def get_index_price(self, index_name: str) -> float:
        url = f"{self.BASE_URL}/get_index_price"
        async with self.session.get(url, params={"index_name": index_name}) as resp:
            data = await resp.json()
            return data["result"]["index_price"]

    async def __aenter__(self) -> "DeribitClient":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.session.close()
