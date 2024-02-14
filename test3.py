import requests


def fetch_user_data(key: str):
    url = f"http://univer.kstu.kz/user/key/{key}/"
    response = requests.post(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}: {response.reason}")
        return None
    else:
        return response.json()


# Пример использования
key = fetch_user_data()
if key is not None:
    print("Полученный ключ:", key)
else:
    print("Не удалось получить ключ")
