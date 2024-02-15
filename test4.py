import requests

url = "http://localhost:8000/get_shedule/"


response = requests.post(url, json=data)

print(response.json())
