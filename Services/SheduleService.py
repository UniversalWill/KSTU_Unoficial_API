import requests
from requests.cookies import cookiejar_from_dict
from Services.AuthService import get_cookie_for_univer
from Services.UserService import User

user = User(username="ivachshenko.gennadiy", password="5t8x9m780265_")


def get_shedule(user):
    url = "http://univer.kstu.kz/student/myschedule/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.5",
        "Referer": "http://univer.kstu.kz/student/bachelor/",
        "Cookie": "user_login=ivachshenko.gennadiy; ASP.NET_SessionId=zcxog54dqvkpeiepqo0dnjc0; .ASPXAUTH=7D08220C7CE70D82A53D9BDCC0DC577BDBF14BA2742A196BB4CE22B539133075CAA5FF701E8F3D0B5AC4186A286D10B9622499E20F4C9CBAF09097FB03A2352ADE0B89275B3C2EBEA05693B0046EF041A7DBBD4BEC46623C1FFB4E13D4A7B3B88FE351DA7C556DD7A806488C4BDE8F3587A1AD7185586C2E81EE3DF2A2BCB0AF732DD58F4D645AA45C99F4482F832FF3B242B429CB653EB448C7593637A3DEAF",
        "Upgrade-Insecure-Requests": "1",
    }

    dict_cookie = get_cookie_for_univer(user.username, user.password)
    cookies = cookiejar_from_dict(dict_cookie)
    session = requests.session()
    session.cookies.update(cookies)
    response = session.get(url, headers=headers)

    print(response.text)
