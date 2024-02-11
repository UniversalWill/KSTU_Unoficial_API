import requests
from bs4 import BeautifulSoup
from .AuthService import get_cookie_for_univer


def get_shedule(user):
    url = "http://univer.kstu.kz/student/myschedule/"
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.5",
        "Referer": "http://univer.kstu.kz/student/bachelor/",
        "Cookie": "user_login=ivachshenko.gennadiy; ASP.NET_SessionId=zcxog54dqvkpeiepqo0dnjc0; .ASPXAUTH=7D08220C7CE70D82A53D9BDCC0DC577BDBF14BA2742A196BB4CE22B539133075CAA5FF701E8F3D0B5AC4186A286D10B9622499E20F4C9CBAF09097FB03A2352ADE0B89275B3C2EBEA05693B0046EF041A7DBBD4BEC46623C1FFB4E13D4A7B3B88FE351DA7C556DD7A806488C4BDE8F3587A1AD7185586C2E81EE3DF2A2BCB0AF732DD58F4D645AA45C99F4482F832FF3B242B429CB653EB448C7593637A3DEAF",
        "Upgrade-Insecure-Requests": "1",
    }

    dict_cookie = get_cookie_for_univer(user)
    session = requests.session()
    session.cookies.update(dict_cookie)
    response = session.get(url, headers=headers)

    schedule_data = {}
    soup = BeautifulSoup(response.text, "html.parser")
    table_element = soup.find("table", class_="schedule")

    for day in days:
        schedule_data[day] = {}
        day_column_index = days.index(day) + 1
        rows = table_element.select(f"tr td:nth-child({day_column_index}) div.groups")

        for row in rows:
            time = row.find_previous("td", class_="time").text.strip()
            course = row.find("p", class_="teacher").text.strip()
            instructor = row.select_one("p.teacher ~ p.teacher").text.strip()
            location = row.select_one("span.aud_faculty + span").text.strip()
            denominator_tag = row.find("span", class_="denominator")
            denominator = (
                denominator_tag.text.strip() if denominator_tag else "Каждая неделя"
            )
            schedule_data[day][course] = {
                "time": time,
                "type": course.split("(")[1][:-1],
                "instructor": instructor,
                "location": location,
                "denominator": denominator,
            }

    return schedule_data
