from typing import Dict
from aiohttp.client import ClientSession, ClientResponseError


class User:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password
        self.session = ClientSession()

    CookieData = Dict[str, str]

    async def fetch_cookies(self, session: ClientSession) -> None | Dict[str, str]:
        try:
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
                        raise Exception("Authentication failed. Invalid credentials.")

        except ClientResponseError as e:
            # Handle ClientResponseError (e.g., HTTP errors)
            print(f"HTTP error: {e}")
            return None

        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            return None
