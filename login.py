from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.core.os_manager import ChromeType
from bs4 import BeautifulSoup
import json

login_url = "https://univer.kstu.kz/user/login"
days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"]


def get_schedule(username, password):
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Login
        driver.get(login_url)
        username_field = driver.find_element(By.XPATH, '//input[@type="text"]')
        password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
        username_field.send_keys(username)
        password_field.send_keys(password + Keys.RETURN)

        # Switch to Russian locale
        driver.get("https://univer.kstu.kz/lang/change/ru/")

        # Get schedule
        driver.get("https://univer.kstu.kz/student/myschedule/")
        table_element = driver.find_element(By.XPATH, '//table[@class="schedule"]')
        table_html = str(table_element.get_attribute("innerHTML"))
        soup = BeautifulSoup(table_html, "html.parser")

        schedule_data = {}

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

                # Determine numerator/denominator
                denominator_tag = row.find("span", class_="denominator")
                denominator = (
                    denominator_tag.text.strip() if denominator_tag else "Каждая неделя"
                )
                print(denominator_tag, "\n", denominator)
                schedule_data[day][course] = {
                    "time": time,
                    "type": course.split("(")[1][:-1],
                    "instructor": instructor,
                    "location": location,
                    "denominator": denominator,
                }

        serialized_schedule = json.dumps(schedule_data, ensure_ascii=False, indent=2)
        print(serialized_schedule)

    finally:
        driver.quit()


# Usage
username = "ivachshenko.gennadiy"
password = "5t8x9m780165_"

get_schedule(username, password)
