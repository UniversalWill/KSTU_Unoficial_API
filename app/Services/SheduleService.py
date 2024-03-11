import json
from typing import Dict, Optional
from bs4 import BeautifulSoup
from fastapi.exceptions import HTTPException

from .HTTPService import HttpService
from .UserService import AuthenticationError, User

ScheduleData = Dict[str, Dict[str, Optional[Dict[str, str]]]]


class SheduleService:
    @staticmethod
    async def get_shedule(login: str, password: str) -> str | None:
        try:
            user: User = User(login, password)
            url: str = "https://univer.kstu.kz/student/myschedule/"
            _headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Chrome/106.0.0.0 Safari/537.36"
                ),
            }

            dict_cookie: Dict[str, str] = await user.fetch_cookies()
            if not dict_cookie:
                raise AuthenticationError

            response = await HttpService.get(url, headers=_headers, cookies=dict_cookie)
            soup = BeautifulSoup(response, "html.parser")
            schedule_data: ScheduleData = {}

            # Получаем дни недели
            days_of_week = soup.find(
                "tr", {"style": "height: 20px; border:1px solid Green"}
            ).find_all("th")
            days = [day.text.strip() for day in days_of_week if day.text.strip()]

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
                    denominator = "Числитель" if denominator_tag else "Знаменатель"

                    schedule_data[day][time] = {
                        "subject": course,
                        "teacher": instructor,
                        "classroom": location,
                        "denominator": denominator
                        if denominator_tag
                        else "Каждая неделя",
                    }

            # Сериализация в JSON и вывод
            serialized_schedule = json.dumps(
                schedule_data, ensure_ascii=False, indent=2
            )

            return serialized_schedule

        except AuthenticationError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
