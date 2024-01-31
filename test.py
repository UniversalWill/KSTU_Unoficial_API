import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from bs4 import BeautifulSoup
import pdb

pdb.set_trace()

app = FastAPI()


class Credentials(BaseModel):
    username: str = "ivachshenko.gennadiy"
    password: str = "5t8x9m780165_"


login_url = "https://univer.kstu.kz/user/login"
schedule_url = "https://univer.kstu.kz/student/myschedule/"
days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]


class AuthService:
    @staticmethod
    def authenticate(username: str, password: str) -> dict:
        options = Options()
        options.page_load_strategy = "eager"
        options.add_argument("--headless")
        service = Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        )
        driver = webdriver.Chrome(service=service, options=options)

        try:
            # Login
            driver.get(login_url)
            username_field = driver.find_element(By.XPATH, '//input[@type="text"]')
            password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.submit()

            # Get cookies
            cookies = {
                cookie["name"]: cookie["value"] for cookie in driver.get_cookies()
            }
            print("Authenticated. Cookies:", cookies)
            return cookies

        finally:
            driver.quit()


class ScheduleService:
    @staticmethod
    def get_schedule(cookies: dict) -> dict:
        session = requests.Session()
        session.cookies.update(cookies)

        # Получение расписания с использованием requests
        response = session.get(schedule_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Ошибка при получении расписания"
            )

        # Обработка HTML-страницы с расписанием
        schedule_data = parse_schedule(response.text)
        print("Schedule data:", schedule_data)
        return schedule_data


def parse_schedule(html):
    schedule_data = {}
    soup = BeautifulSoup(html, "html.parser")
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


@app.post("/authenticate/")
def authenticate_user(credentials: Credentials):
    return AuthService.authenticate(credentials.username, credentials.password)


@app.get("/schedule/")
def get_schedule(cookies: dict):
    return ScheduleService.get_schedule(cookies)
