from bs4 import BeautifulSoup

html_content = """
User
<tr class="top">
                <td class="lt"></td>
                <td class="ct" unselectable="on">
                    Cryptographic information security systems ([RK1 + RK2 + Exam] (100)) 15.01.2024 - 20.03.2024
                </td>
                <td class="rt"></td>
            </tr>
                        <tr class="mid">
                            <td class="lt"></td>
                            <td class="ts">
                                <a href="http://univer.kstu.kz/student/attendance/show/210940/2023/2" title="View full log of attendance" class="lt">
                                    Lecture - Мурых Е. Л. (Russian )                                      
                                </a>
                            </td>
                            <td class="rt"></td>
                        </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK1 (100)">RK1 (100)</th>
                                                <th style="width:30px;">16.01</th>
                                                <th style="width:30px;">23.01</th>
                                                <th style="width:30px;">30.01</th>
                                                <th style="width:30px;">06.02</th>
                                                <th style="width:30px;">13.02</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">1</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">1</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">2</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK2 (100)">RK2 (100)</th>
                                                <th style="width:30px;">20.02</th>
                                                <th style="width:30px;">05.03</th>
                                                <th style="width:30px;">12.03</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">n</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">0</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                        <tr class="mid">
                            <td class="lt"></td>
                            <td class="ts">
                                <a href="http://univer.kstu.kz/student/attendance/show/210941/2023/2" title="View full log of attendance" class="lt">
                                    Laboratory work - Мурых Е. Л. (Russian )                                      
                                </a>
                            </td>
                            <td class="rt"></td>
                        </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK1 (100)">RK1 (100)</th>
                                                <th style="width:30px;">19.01</th>
                                                <th style="width:30px;">26.01</th>
                                                <th style="width:30px;">02.02</th>
                                                <th style="width:30px;">09.02</th>
                                                <th style="width:30px;">15.02</th>
                                                <th style="width:30px;">16.02</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">2</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">1</td>
                                                <td style="text-align:center" title="">11</td>
                                                <td style="text-align:center" title="">11</td>
                                                <td style="text-align:center" title="">15</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">40</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK2 (100)">RK2 (100)</th>
                                                <th style="width:30px;">23.02</th>
                                                <th style="width:30px;">01.03</th>
                                                <th style="width:30px;">07.03</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">5</td>
                                                <td style="text-align:center" title="">10</td>
                                                <td style="text-align:center" title="">10</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">25</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                        <tr class="mid">
                            <td class="lt"></td>
                            <td class="ts">
                                <a href="http://univer.kstu.kz/student/attendance/show/210943/2023/2" title="View full log of attendance" class="lt">
                                    IWST - Мурых Е. Л. (Russian )                                      
                                </a>
                            </td>
                            <td class="rt"></td>
                        </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK1 (100)">RK1 (100)</th>
                                                <th style="width:30px;">16.01</th>
                                                <th style="width:30px;">17.01</th>
                                                <th style="width:30px;">23.01</th>
                                                <th style="width:30px;">30.01</th>
                                                <th style="width:30px;">07.02</th>
                                                <th style="width:30px;">10.02</th>
                                                <th style="width:30px;">13.02</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">20</td>
                                                <td style="text-align:center" title="">10</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">30</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK2 (100)">RK2 (100)</th>
                                                <th style="width:30px;">20.02</th>
                                                <th style="width:30px;">29.02</th>
                                                <th style="width:30px;">05.03</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">10</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">10</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                        <tr class="mid">
                            <td class="lt"></td>
                            <td class="ts">
                                <a href="http://univer.kstu.kz/student/attendance/show/216567/2023/2" title="View full log of attendance" class="lt">
                                    Seminar - Мурых Е. Л. (Russian )                                      
                                </a>
                            </td>
                            <td class="rt"></td>
                        </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK1 (100)">RK1 (100)</th>
                                                <th style="width:30px;">17.01</th>
                                                <th style="width:30px;">24.01</th>
                                                <th style="width:30px;">07.02</th>
                                                <th style="width:30px;">10.02</th>
                                                <th style="width:30px;">14.02</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">2</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">1</td>
                                                <td style="text-align:center" title="">10</td>
                                                <td style="text-align:center" title="">10</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">23</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
                    <tr class="mid">
                        <td class="lt"></td>
                        <td class="tt">
                             
                                    <table class="inner" cellpadding="0" cellspacing="0">
                                        <tbody><tr>
                                            <th style="width:30px;" rowspan="2" title="RK2 (100)">RK2 (100)</th>
                                                <th style="width:30px;">20.02</th>
                                                <th style="width:30px;">28.02</th>
                                                <th style="width:30px;">05.03</th>
                                                <th style="width:30px;">06.03</th>
                                            <th>&nbsp;</th>
                                            <th style="width:45px;text-align:center">sum</th>

                                        </tr>
                                        <tr>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">5</td>
                                                <td style="text-align:center" title="">0</td>
                                                <td style="text-align:center" title="">1</td>
                                            <td>&nbsp;</td>
                                            <td style="text-align:center;font-weight:bold;">6</td>

                                        </tr>
                                    </tbody></table>
                                 
                        </td>
                        <td class="rt"></td>
                    </tr>
            <tr class="mid">
                <td class="lt"></td>
                <td class="ct">
                        <b>RK1 (100): </b>95                        <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
                        <b>RK2 (100): </b>41                        <span>&nbsp;&nbsp;&nbsp;&nbsp;</span>
                </td>
                <td class="rt"></td>
            </tr>"""

soup = BeautifulSoup(html_content, "html.parser")

# Ищем строки с классом "mid"
rows = soup.find_all("tr", class_="mid")

# Создаем пустой словарь для хранения результатов оценок
grades = {"RK1": [], "RK2": []}

# Проходимся по каждой строке
for row in rows:
    print("Найдена строка:")
    print(row)

    # Ищем ячейку с классом "ct"
    ct_cell = row.find("td", class_="ct")
    print("Найдена ячейка ct:")
    print(ct_cell)

    # Проверяем, существует ли ячейка с классом "ct"
    if ct_cell:
        # Получаем текст из ячейки "ct"
        text = ct_cell.get_text(strip=True)
        print("Текст ячейки ct:")
        print(text)

        # Извлекаем оценки из текста ячейки ct
        parts = text.split()
        for part in parts:
            if "RK1" in part:
                rk1_score = "".join(filter(str.isdigit, part))
                grades["RK1"].append(int(rk1_score))
                print("Оценка RK1:", int(rk1_score))
            elif "RK2" in part:
                rk2_score = "".join(filter(str.isdigit, part))
                grades["RK2"].append(int(rk2_score))
                print("Оценка RK2:", int(rk2_score))

# Выводим результаты оценок
print("Оценки RK1:", grades["RK1"])
print("Оценки RK2:", grades["RK2"])
