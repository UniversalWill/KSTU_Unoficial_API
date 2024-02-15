from aiohttp import ClientSession
from bs4 import BeautifulSoup

from Services.UserService import User


async def get_shedule(login, password):
    user = User(login, password)
    url = "http://univer.kstu.kz/student/myschedule/"
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.5",
        "Referer": "http://univer.kstu.kz/student/bachelor/",
        "Upgrade-Insecure-Requests": "1",
    }

    async with ClientSession() as session:
        dict_cookie = await user.fetch_cookies(session)
        if dict_cookie:
            async with session.get(
                url, headers=headers, cookies=dict_cookie
            ) as response:
                schedule_data = {}
                soup = BeautifulSoup(await response.text(), "html.parser")
                table_element = soup.find("table", class_="schedule")

                for day in days:
                    schedule_data[day] = {}
                    day_column_index = days.index(day) + 1
                    rows = table_element.select(
                        f"tr td:nth-child({day_column_index}) div.groups"
                    )

                    for row in rows:
                        time = row.find_previous("td", class_="time").text.strip()
                        course = row.find("p", class_="teacher").text.strip()
                        instructor = row.select_one(
                            "p.teacher ~ p.teacher"
                        ).text.strip()
                        location = row.select_one(
                            "span.aud_faculty + span"
                        ).text.strip()
                        denominator_tag = row.find("span", class_="denominator")
                        denominator = (
                            denominator_tag.text.strip()
                            if denominator_tag
                            else "Каждая неделя"
                        )
                        schedule_data[day][course] = {
                            "time": time,
                            "type": course.split("(")[1][:-1],
                            "instructor": instructor,
                            "location": location,
                            "denominator": denominator,
                        }
                return schedule_data
