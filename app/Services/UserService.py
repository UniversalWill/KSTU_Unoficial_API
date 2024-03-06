from typing import Dict

from aiohttp.client import ClientSession
from fastapi.exceptions import HTTPException


class AuthenticationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials")


class User:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
        self.session = ClientSession()

    CookieData = Dict[str, str]

    async def fetch_cookies(self, session: ClientSession) -> None | Dict[str, str]:
        async with self.session as session:
            async with session.get(
                f"https://univerapi.kstu.kz/?login={self.login}&password={self.password}"
            ) as response:
                cookies = response.cookies
                aspxauth_cookie = cookies.get(".ASPXAUTH")
                sessionid_cookie = cookies.get("ASP.NET_SessionId")
                if aspxauth_cookie and sessionid_cookie:
                    return {
                        ".ASPXAUTH": aspxauth_cookie.value,
                        "ASP.NET_SessionId": sessionid_cookie.value,
                    }
                else:
                    raise AuthenticationError()
