from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from datetime import date
import os
import datetime
from datetime import datetime, timedelta
while True:
    ned = 0 
    # Заданная дата начала (02.09.2024)
    start_date = datetime.strptime("02.09.2024", "%d.%m.%Y")

    # Текущая дата
    current_date = datetime.now()

    # Разница между текущей датой и заданной
    delta = current_date - start_date

    # Номер недели
    week_number1 = delta.days // 7  + 1 # Плюс 1, чтобы отсчитать с первой недели
    with open("C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайты/current.txt", "w", encoding="utf-8") as file:#куда сохронять номер нынешнего дня !!!!!!!!!!!!!!!
        file.write(str(week_number1)) 
    

     

    for ned in range(0,52):
        
        site = f"https://rasp.tpu.ru/gruppa_39208/2024/{ned}/view.html"  
        driver = webdriver.Chrome()  
        driver.get(site)
        time.sleep(3)  # подождать, пока страница полностью загрузится
        html = driver.page_source
        url = site
        response = requests.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        file_path = f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайты/{ned}.html"#куда все дни !!!!!!!!!
        rows = soup.select("table.timetable tr th")
        for row in rows:
            tiiime = soup.select_one("th.text-center") 
            full_text = row.get_text(separator=" ", strip=True)
            date_only = full_text.split()[0]  # берём первую часть — дату  # текст текущего th
            today = date.today()
            print(today.strftime("%d.%m.%y"),date_only)
            # if date_only == today.strftime("%d.%m.%y"):
            #     with open("C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайты/current.txt", "w", encoding="utf-8") as file:#куда сохронять номер нынешнего дня !!!!!!!!!!!!!!!
            #         file.write(str(ned)) 
        if soup.select_one("html head title").text != "504 Gateway Time-out" and response.status_code == 200:

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html)    
            print("Сохранилось")
            ned += 1
        else: 
            print("Сайту плохо")
    driver.quit()

    import os
    from bs4 import BeautifulSoup
    import re

    # Базовый путь для сохранения
    base_path = r"C:\Users\vladi\OneDrive\Документы\pyton\tg botara\сайтыобработка"
    old_allweeks = "C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайты/old_allweeks.txt"
    peremena_file_path = "C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/peremena.txt"

    # Массив дней недели
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    def is_schedule_updated(old_file, new_file):
        if not os.path.exists(old_file):
            return True  # Если старый файл не существует, считаем, что расписание обновлено

        with open(old_file, "r", encoding="utf-8") as f1, open(new_file, "r", encoding="utf-8") as f2:
            old_schedule = f1.read()
            new_schedule = f2.read()

        return old_schedule != new_schedule  # Возвращаем True, если содержимое файлов отличается

    # Создание папок для недель 0–50
    for week_num in range(51):
        week_path = os.path.join(base_path, str(week_num))
        os.makedirs(week_path, exist_ok=True)

        # Чтение и обработка файла
        path = f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайты/{week_num}.html"
        with open(path, "r", encoding="utf-8") as html:
            soup = BeautifulSoup(html, "lxml")
            rows = soup.find_all('tr')

            # Извлечение дат из заголовков таблицы
            date_headers = soup.select("table.timetable thead tr th.text-center")
            dates = []
            for header in date_headers[1:7]:  # Пропускаем первый заголовок (Время), берём следующие 6 (дни недели)
                # Извлекаем только дату (например, "07.04.25") с помощью регулярного выражения
                header_text = header.get_text(strip=True)
                date_match = re.search(r'\d{2}\.\d{2}\.\d{2}', header_text)
                if date_match:
                    dates.append(date_match.group(0))
                else:
                    dates.append("Неизвестная дата")

            # Словарь для хранения расписания по дням
            # Словарь для хранения расписания по дням
            week_schedule = {i: {} for i in range(1, 7)}
            allweek_schedule = {}

            # Найдём все строки с расписанием
            rows = soup.select("table.timetable tbody tr")

            # Поддержка правильного распределения по дням
            col_skip = [0] * 6  # трекер rowspan по каждому дню

            for row in rows:
                cells = row.find_all("td", recursive=False)
                if not cells:
                    continue

                # Первая ячейка — это время
                time_cell = next((cell for cell in cells if cell.has_attr("title")), None)
                if not time_cell:
                    continue
                time_range = time_cell["title"]

                col = 0
                for cell in cells:
                    if cell.has_attr("title"):
                        continue  # skip time cell

                    # Пропускаем "пустые" столбцы (занятые `rowspan` с предыдущих строк)
                    while col < 6 and col_skip[col] > 0:
                        col_skip[col] -= 1
                        col += 1

                    if col >= 6:
                        break

                    # Обработка rowspan
                    rowspan = int(cell.get("rowspan", 1))
                    if rowspan > 1:
                        col_skip[col] = rowspan - 1

                    # Пропуск праздников
                    if 'free-day' in cell.get("class", []):
                        col += 1
                        continue

                    if not cell.text.strip():
                        col += 1
                        continue

                    subjects = cell.find_all('span', title=True)
                    if not subjects:
                        # Альтернатива: попробовать найти по структуре <a> + <b>
                        alt_a = cell.find('a', class_="green")
                        alt_b = cell.find('b', title=True)

                        if not alt_a or not alt_b:
                            col += 1
                            continue

                        subject = alt_a.get_text(strip=True)
                        subjectStyle = alt_b.get("title", "Пусто")

                        teacher_tag = cell.find_all('a', class_="green")
                        teacher = teacher_tag[1].get_text(strip=True) if len(teacher_tag) > 1 else "Пусто"

                        room_info = teacher_tag[2:4] if len(teacher_tag) >= 4 else []
                        if len(room_info) == 2:
                            building = room_info[0].get_text(strip=True)
                            room = room_info[1].get_text(strip=True)
                        else:
                            building = "—"
                            room = "—"

                        if teacher == "Пусто":
                            teacher = "—"

                        lesson_str = f"{subject} ({subjectStyle}) {teacher}, к. {building} ауд. {room}"

                        if time_range not in week_schedule[col + 1]:
                            week_schedule[col + 1][time_range] = []
                        week_schedule[col + 1][time_range].append(lesson_str)

                        if time_range not in allweek_schedule:
                            allweek_schedule[time_range] = []
                        allweek_schedule[time_range].append(lesson_str)

                        col += 1
                        continue
        

                    for subject_elem in subjects:
                        subject = subject_elem.get("title", "Пусто")

                        subjectStyle_elem = subject_elem.find_next('b', title=True)
                        subjectStyle = subjectStyle_elem.get_text(strip=True) if subjectStyle_elem else "Пусто"

                        teacher_tag = subject_elem.find_next('a', class_="green")
                        teacher = teacher_tag.get_text(strip=True) if teacher_tag else "Пусто"

                        room_info = teacher_tag.find_all_next('a', class_='green')[:2] if teacher_tag else []
                        if len(room_info) == 2:
                            building = room_info[0].get_text(strip=True)
                            room = room_info[1].get_text(strip=True)
                            if teacher in [building, room] or not building or not room:
                                building = "?"
                                room = "?"
                        else:
                            building = "?"
                            room = "?"

                        if "Пусто" in [subject, subjectStyle, teacher] or "?" in [building, room]:
                            continue

                        lesson_str = f"{subject} ({subjectStyle}) {teacher}, к. {building} ауд. {room}"

                        if time_range not in week_schedule[col + 1]:
                            week_schedule[col + 1][time_range] = []
                        week_schedule[col + 1][time_range].append(lesson_str)

                        if time_range not in allweek_schedule:
                            allweek_schedule[time_range] = []
                        allweek_schedule[time_range].append(lesson_str)

                    col += 1

            # Сохранение расписания для каждого дня с датой
            for day_num in range(1, 7):
                with open(os.path.join(week_path, f"{day_num}.txt"), "w", encoding="utf-8") as f:
                    f.write(f"{days[day_num - 1]} ({dates[day_num - 1]}):\n\n")
                    for time_range, lessons in week_schedule[day_num].items():
                        f.write(f"{time_range}\n")
                        for lesson in lessons:
                            f.write(f"  {lesson}\n")
                        f.write("\n")

            # Сохранение расписания всей недели с датами
            with open(os.path.join(week_path, "allweek.txt"), "w", encoding="utf-8") as f:
                for day_num in range(1, 7):
                    f.write(f"{days[day_num - 1]} ({dates[day_num - 1]}):\n\n")
                    for time_range, lessons in week_schedule[day_num].items():
                        f.write(f"{time_range}\n")
                        for lesson in lessons:
                            f.write(f"  {lesson}\n")
                        f.write("\n")
                f.write("\n")

    # Сохранение всех недель в один файл
    all_weeks_path = os.path.join(base_path, "allweeks.txt")
    with open(all_weeks_path, "w", encoding="utf-8") as f:
        for week_num in range(51):
            f.write(f"Неделя {week_num}\n\n")
            week_path = os.path.join(base_path, str(week_num), "allweek.txt")
            if os.path.exists(week_path):
                with open(week_path, "r", encoding="utf-8") as week_file:
                    f.write(week_file.read())
                f.write("\n")

    # Проверка, было ли обновление расписания
    if is_schedule_updated(old_allweeks, all_weeks_path):
        print("Расписание обновлено!")
        if os.path.exists(old_allweeks):
            os.remove(old_allweeks)  # Удаляем старый файл, если он существует
        os.rename(all_weeks_path, old_allweeks)  # Переименовываем новый файл
        with open(peremena_file_path, "w", encoding="utf-8") as peremena_file:
            peremena_file.write("true")  # Записываем "true", если расписание обновилось
    else:
        print("Нет изменений в расписании.")
        with open(peremena_file_path, "w", encoding="utf-8") as peremena_file:
            peremena_file.write("false")  # Записываем "false", если изменений нет
    time.sleep(6 * 60 * 60)  


