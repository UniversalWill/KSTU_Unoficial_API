from aiohttp.client import ClientSession
from typing import Optional, Dict

from aiohttp.client_exceptions import ClientConnectorError, InvalidURL

_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/106.0.0.0 Safari/537.36"
    ),
}


class HttpRequestError(Exception):
    "Http request error"


class HttpService:
    headers = _headers

    @staticmethod
    async def get(url: str, cookies: Dict[str, str], headers: Optional[dict] = headers):
        async with ClientSession() as session:
            try:
                async with session.get(
                    url, headers=headers, cookies=cookies
                ) as response:
                    return await response.text()
            except (ClientConnectorError, InvalidURL):
                raise HttpRequestError

    @staticmethod
    async def extract_cookies(url: str, headers: Optional[dict] = headers):
        async with ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    return response.cookies
            except ClientConnectorError:
                raise HttpRequestError
