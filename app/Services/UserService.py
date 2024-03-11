from typing import Dict

from fastapi.exceptions import HTTPException

from app.Services.HTTPService import HttpService


class AuthenticationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid credentials")


class User:
    def __init__(self, login: str, password: str) -> None:
        self.login = login
        self.password = password

    async def fetch_cookies(self) -> Dict[str, str]:
        url = f"https://univerapi.kstu.kz/?login={self.login}&password={self.password}"
        try:
            cookies = await HttpService.extract_cookies(url)
            aspxauth_cookie = cookies.get(".ASPXAUTH")
            sessionid_cookie = cookies.get("ASP.NET_SessionId")
            if aspxauth_cookie and sessionid_cookie:
                return {
                    ".ASPXAUTH": aspxauth_cookie.value,
                    "ASP.NET_SessionId": sessionid_cookie.value,
                }
            else:
                raise AuthenticationError()
        except Exception:
            raise AuthenticationError()
