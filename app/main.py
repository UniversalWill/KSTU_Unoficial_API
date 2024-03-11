from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

from .Services.JournalService import JournalService
from app.Services.SheduleService import SheduleService


app = FastAPI()


class UserCredentials(BaseModel):
    login: str
    password: str


@app.post("/get_shedule/")
async def get_schedule_endpoint(credentials: UserCredentials):
    """
    Получить расписание для пользователя.

    Параметры:
        - credentials: данные пользователя (login, password)

    Возвращает:
    - расписание в формате JSON
    """
    return await SheduleService.get_shedule(credentials.login, credentials.password)


@app.post("/get_journal")
async def get_openapi_endpoint(credentials: UserCredentials):
    return await JournalService.get_journal(credentials.login, credentials.password)


# Генерация документации OpenAPI с помощью FastAPI.openapi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is a very cool API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Установка документации OpenAPI и включение Swagger UI
app.openapi = custom_openapi
