from aiohttp.client import ClientSession
from typing import Dict


class HTTPService:
    def __init__(self) -> None:
        self.session = ClientSession()

    async def fetch(
        self, url: str, headers: Dict[str, str], cookies: Dict[str, str]
    ) -> str:
        async with self.session.get(url, headers=headers, cookies=cookies) as response:
            return await response.text()

    async def close_session(self) -> None:
        await self.session.close()
