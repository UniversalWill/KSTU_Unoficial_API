from requests.sessions import Session
import re


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_payload_form_js(self):
        ses = Session()
        request = ses.get("http://univer.kstu.kz/user/login")
        js_text = request.text

        pattern_all_attr = r'\_\w+\.attr\("([^"]+)", \'([^\']+)\'\)'
        matches = re.findall(pattern_all_attr, js_text)
        for i in matches:
            print(i)
        return js_text

    def transform_data(self, t, k):
        a = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        table = [a[i:] + a[:i] for i in range(len(a))]
        p4jgkvy = ""
        for i in range(len(t)):
            if t[i] in a:
                p4jgkvy += table[a.index(k[i])][a.index(t[i])]
            else:
                p4jgkvy += t[i]
        return p4jgkvy


pattern = r"./user/key/(\d+)/"
matches = re.findall(pattern, string)

if matches:
    print(matches[0])  # Выводим первое найденное значение после /user/key/
else:
    print("Значение после /user/key/ не найдено.")
