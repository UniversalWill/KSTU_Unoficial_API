import json
from bs4 import BeautifulSoup
# Для обработки исходного HTML используем BeautifulSoup для парсинга и создания структурированного JSON

html_content = """
<tr class="top">
    <td class="lt"></td>
    <td class="ct" unselectable="on">Криптографические системы защиты информации ([РК1 + РК2 + Экз] (100)) 15.01.2024 - 20.03.2024</td>
    <td class="rt"></td>
</tr>
<tr class="mid">
    <td class="lt"></td>
    <td class="ts">
        <a href="#" title="Лекция">Лекция - Мурых Е. Л. (Русский)</a>
    </td>
    <td class="rt"></td>
</tr>
<tr class="mid">
    <td class="lt"></td>
    <td class="tt">
        <table class="inner" cellpadding="0" cellspacing="0">
            <tbody><tr>
                <th rowspan="2">РК1 (100)</th>
                <th>16.01</th>
                <th>23.01</th>
                <th>30.01</th>
                <th>06.02</th>
                <th>13.02</th>
                <th>Сумма</th>
            </tr>
            <tr>
                <td>1</td>
                <td>0</td>
                <td>1</td>
                <td>0</td>
                <td>н</td>
                <td>2</td>
            </tr></tbody>
        </table>
    </td>
    <td class="rt"></td>
</tr>
<!-- Пример для РК2 и других типов занятий опущен для краткости -->
"""

# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, "html.parser")

# Словарь для хранения данных
data = {}

# Название предмета
subject_name = soup.find("td", class_="ct").text.strip()
data[subject_name] = {}

# Поиск всех занятий
activities = soup.find_all("tr", class_="mid")

for activity in activities:
    activity_type_tag = activity.find("a")
    if activity_type_tag:
        activity_type = activity_type_tag.text.strip()
        data[subject_name][activity_type] = {}

        # Следующий элемент в DOM - таблица с оценками
        grades_table = activity.find_next_sibling("tr", class_="mid").find(
            "table", class_="inner"
        )
        if grades_table:
            for grade_type_row in grades_table.find_all("th", rowspan=True):
                grade_type = grade_type_row.text.strip()
                data[subject_name][activity_type][grade_type] = {}

                dates = grades_table.find_all("th")[
                    1:-1
                ]  # Пропускаем первую и последнюю колонку ("РК1", "Сумма")
                grades = grade_type_row.find_next_siblings("td")[
                    :-1
                ]  # Пропускаем последнюю ячейку с суммой

                for date, grade in zip(dates, grades):
                    date_text = date.text.strip()
                    grade_text = grade.text.strip()
                    data[subject_name][activity_type][grade_type][
                        date_text
                    ] = grade_text

# Преобразуем словарь в JSON
json_output = json.dumps(data, ensure_ascii=False, indent=4)
print(json_output)
