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
                        return None

        except ClientResponseError as e:
            # Handle ClientResponseError (e.g., HTTP errors)
            print(f"HTTP error: {e}")
            return None

        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")
            return None

    # def get_payload(self):
    #     request = self.session.get("http://univer.kstu.kz/user/login")
    #     string = request.text
    #     payload = {}
    #
    #     regex_name = r'\_\w+\.attr\("name", \'([^\']+)\'\)'
    #     regex_value = r'_\w+\.attr\("value", \'([^\']*)\'\s*\)'
    #     regex_key = r"./user/key/(\d+)/"
    #
    #     name_matches = re.findall(regex_name, string)
    #     value_matches = re.findall(regex_value, string)
    #     key_matches = re.findall(regex_key, string)
    #
    #     key_for_encrypt = self.fetch_user_crypto_key(str(key_matches[0]))
    #     encrypt_login = self.vigenere_cipher(self.login, key_for_encrypt)
    #     encrypt_password = self.vigenere_cipher(self.password, key_for_encrypt)
    #
    #     value_matches.insert(0, encrypt_login)
    #     value_matches.insert(2, encrypt_password)
    #
    #     for name, value in zip(name_matches, value_matches):
    #         payload[name] = value
    #
    #     return payload
    #
    # def vigenere_cipher(self, text, key):
    #     alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #     table = ["" for _ in range(len(alphabet))]
    #     for i in range(len(alphabet)):
    #         table[i] = alphabet[i:] + alphabet[:i]
    #
    #     encrypted_text = ""
    #     key_repeated = ""
    #     while len(key_repeated) < len(text):
    #         key_repeated += key
    #
    #     for i in range(len(text)):
    #         if text[i] in alphabet:
    #             encrypted_text += table[alphabet.index(key_repeated[i])][
    #                 alphabet.index(text[i])
    #             ]
    #         else:
    #             encrypted_text += text[i]
    #
    #     return encrypted_text
    #
    # def fetch_user_crypto_key(self, key: str) -> str | None:
    #     url = f"http://univer.kstu.kz/user/key/{key}/"
    #     response = post(url)
    #
    #     if response.status_code != 200:
    #         print(f"Error: {response.status_code}: {response.reason}")
    #         return None
    #     else:
    #         return response.json()
    #
    # def auth_session(self):
    #     URL = "https://univer.kstu.kz/user/login/"
    #     payload = self.get_payload()
    #     print(payload)
    #     auth_post = self.session.post(url=URL, data=self.get_payload())
    #     return auth_post.cookies
