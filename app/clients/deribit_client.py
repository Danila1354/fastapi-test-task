import aiohttp


class DeribitClient:
    BASE_URL = "https://test.deribit.com/api/v2/public"

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get_index_price(self, index_name: str) -> float:
        url = f"{self.BASE_URL}/get_index_price"

        async with self.session.get(url, params={"index_name": index_name}) as resp:
            data = await resp.json()
            return data["result"]["index_price"]

    async def close(self):
        await self.session.close()


async def main():
    client = DeribitClient()

    btc = await client.get_index_price("btc_usd")
    eth = await client.get_index_price("eth_usd")

    print(btc, eth)

    await client.close()
