from aiohttp.client import ClientResponse, ClientSession
from typing import Dict


class HTTPService:
    def __init__(self) -> None:
        self.session = ClientSession()

    async def fetch(
        self,
        url: str,
        headers: None | Dict[str, str] = None,
        cookies: None | Dict[str, str] = None,
    ) -> ClientResponse:
        async with self.session.get(url, headers=headers, cookies=cookies) as response:
            return response

    async def close_session(self) -> None:
        await self.session.close()

    # async def fetch_cookies(
    #     self,
    #     url: str,
    #     headers: None | Dict[str, str] = None,
    #     cookies: None | Dict[str, str] = None,
    # ):
    #     async with self.session.get(url, headers=headers, cookies=cookies) as response:
    #         return response.cookies
