from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.core.os_manager import ChromeType
from selenium.common.exceptions import NoSuchElementException
import json


def get_cookie_for_auth(username: str, password: str) -> str:
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(service=service, options=options)

    login_url = "https://univer.kstu.kz/user/login"

    driver.get(login_url)

    username_field = driver.find_element(By.XPATH, '//input[@type="text"]')
    password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
    username_field.send_keys(username)
    password_field.send_keys(password + Keys.RETURN)
    try:
        driver.find_element(
            By.XPATH,
            "//table[@class='mt']//tr[@class='mid'][2]//td[@class='ct warning']",
        )
        return "Неверное сочетание логина и пароль"
    except NoSuchElementException:
        cookie_data = driver.get_cookies()
        cookie_values = {}

        for cookie in cookie_data:
            name = cookie.get("name")
            value = cookie.get("value")
            if name in [".ASPXAUTH", "ASP.NET_SessionId", "user_login"]:
                cookie_values[name] = value

        json_cookie = json.dumps(cookie_values)
        return json_cookie
