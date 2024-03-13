import json
from typing import Dict
from bs4 import BeautifulSoup
from fastapi.exceptions import HTTPException

from .HTTPService import HttpService
from .UserService import AuthenticationError, User


class JournalService:
    @staticmethod
    async def get_journal(login: str, password: str) -> str | None:
        try:
            user = User(login, password)
            url = "http://univer.kstu.kz/student/attendance/full/"
            _headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Chrome/106.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "ru-RU,ru;q=0.5",
            }

            dict_cookie: Dict[str, str] = await user.fetch_cookies()
            if not dict_cookie:
                raise AuthenticationError

            response = await HttpService.get(url, headers=_headers, cookies=dict_cookie)
            journal_data = {}
            soup = BeautifulSoup(response, "html.parser")

            subject_elements = soup.find_all(
                "td", class_="ct", unselectable="on"
            )  # Находим все элементы с названием предметов

            for subject_element in subject_elements:
                print(subject_element)
                subject = (
                    subject_element.get_text(strip=True).split("[")[0].strip()
                )  # Извлекаем название предмета
                print(subject)
                if subject.endswith("("):
                    subject = subject[:-1]
                print(subject)
                scores_element = subject_element.find_next(
                    "td", class_="ct"
                )  # Находим элемент с баллами предмета
                print(scores_element)

                scores_text = scores_element.get_text(
                    strip=True
                )  # Получаем текст с баллами
                print(scores_text)

                # # Извлекаем баллы РК1
                # rk1_score = ""
                # rk1_index = scores_text.find("РК1 (100):")
                # if rk1_index != -1:
                #     rk1_score = (
                #         scores_text[rk1_index + len("РК1 (100):") :].split()[0].strip()
                #     )
                #
                # # Извлекаем баллы РК2, начиная поиск с позиции, где начинается РК2
                # rk2_score = ""
                # rk2_index = scores_text.find("РК2 (100):")
                # if rk2_index != -1:
                #     rk2_score = (
                #         scores_text[rk2_index + len("РК2 (100):") :].split()[0].strip()
                #     )
                #
                # if rk1_score.endswith("РК2"):
                #     rk1_score = rk1_score[:-3]
                # # Добавляем данные в расписание
                journal_data = scores_text

            # Сериализация в JSON и вывод
            serialized_journal = json.dumps(journal_data, ensure_ascii=False, indent=2)
            return serialized_journal

        except AuthenticationError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
