import json
from typing import Dict
from bs4 import BeautifulSoup, Tag
from fastapi.exceptions import HTTPException

from .UserService import AuthenticationError, User
from .HTTPService import HttpService


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
            print(dict_cookie)
            if not dict_cookie:
                raise AuthenticationError

            response = await HttpService.get(url, headers=_headers, cookies=dict_cookie)
            serialized_journal = {}
            soup = BeautifulSoup(response, "html.parser")
            links = soup.find_all("a")
            # print(links)

            table_with_notes = None
            for l in links:
                if l["href"].startswith("/student/attendance/show/"):
                    table_with_notes = l.parent.parent.parent
                    break

            if not table_with_notes:
                raise ValueError("couldnt found table with notes")

            subjects = {}
            current_subject_name = ""
            current_subject_type = ""
            current_rk = ""
            for row in list(table_with_notes.children):
                if type(row) is Tag and row.has_attr("class") and "top" in row["class"]:
                    current_subject_name = row.find_all(class_="ct")[0].text.strip()
                    print("current_subject_name", current_subject_name)
                    print(row)
                    subjects[current_subject_name] = {}
                    continue

                if type(row) is Tag and len(links := row.find_all("a")) > 0:
                    current_subject_type = links[0].text.strip()
                    subjects[current_subject_name][current_subject_type] = {}
                    continue

                if not row.text.strip():
                    continue

                if len(trs := row.find_all("tr")) > 0:
                    current_rk = trs[0].find_all("th")[0].text
                    subjects[current_subject_name][current_subject_type][
                        current_rk
                    ] = {}

                    dates = list(
                        map(lambda x: x.text, list(trs[0].find_all("th"))[1:-2])
                    )
                    for i, note_tag in enumerate(list(trs[1].find_all("td")[:-2])):
                        note = note_tag.text
                        if not note_tag.text == "н":
                            note = int(note_tag.text)

                        subjects[current_subject_name][current_subject_type][
                            current_rk
                        ][dates[i]] = note

            # Сериализация в JSON и вывод
            serialized_journal = (
                json.dumps(subjects, ensure_ascii=False, indent=2)
                .encode()
                .decode("unicode_escape")
            )
            return serialized_journal

        except AuthenticationError as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
