import json
from typing import Dict, Optional
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fastapi.exceptions import HTTPException
from .UserService import AuthenticationError, User

ScheduleData = Dict[str, Dict[str, Optional[Dict[str, str]]]]


async def get_shedule(login: str, password: str) -> str | None:
    try:
        user: User = User(login, password)
        url: str = "http://univer.kstu.kz/student/myschedule/"
        headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.5",
            "Referer": "http://univer.kstu.kz/student/bachelor/",
            "Upgrade-Insecure-Requests": "1",
        }

        async with ClientSession() as session:
            dict_cookie: Dict[str, str] | None = await user.fetch_cookies(session)
            if dict_cookie:
                async with session.get(
                    url, headers=headers, cookies=dict_cookie
                ) as response:
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    schedule_data: ScheduleData = {}

                    # Получаем дни недели
                    days_of_week = soup.find(
                        "tr", {"style": "height: 20px; border:1px solid Green"}
                    ).find_all("th")
                    days = [
                        day.text.strip() for day in days_of_week if day.text.strip()
                    ]

                    for day in days:
                        schedule_data[day] = {}

                        rows = soup.select(
                            f"tr td.field:nth-child({days.index(day) + 2}) div.groups"
                        )

                        for row in rows:
                            time = row.find_previous("td", class_="time").text.strip()
                            course = row.find("p", class_="teacher").text.strip()
                            instructor = (
                                row.find("p", class_="teacher")
                                .find_next("p", class_="teacher")
                                .text.strip()
                            )
                            location = (
                                row.find("span", class_="aud_faculty")
                                .find_next("span")
                                .text.strip()
                            )

                            # Определение числитель/знаменатель
                            denominator_tag = row.find("p", class_="denominator")
                            denominator = (
                                "Числитель" if denominator_tag else "Знаменатель"
                            )

                            schedule_data[day][time] = {
                                "subject": course,
                                "teacher": instructor,
                                "classroom": location,
                                "period": "Период с 15.01 по 20.03",
                                "denominator": denominator
                                if denominator_tag
                                else "Каждая неделя",
                            }

                    # Сериализация в JSON и вывод
                    serialized_schedule = json.dumps(
                        schedule_data, ensure_ascii=False, indent=2
                    )

                    return serialized_schedule

            return "Authentication failed. Invalid credentials."

    except AuthenticationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
