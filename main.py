from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from Services.SheduleService import get_shedule

app = FastAPI()


class UserCredentials(BaseModel):
    login: str
    password: str


@app.post("/get_shedule/")
async def get_schedule_endpoint(credentials: UserCredentials):
    """
    Получить расписание для пользователя.

    Параметры:
    - credentials: данные пользователя (логин и пароль)

    Возвращает:
    - расписание в формате JSON
    """
    return await get_shedule(credentials.login, credentials.password)


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
