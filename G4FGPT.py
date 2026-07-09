import re
import datetime
import dateparser
import g4f
from g4f import ChatCompletion
from datetime import datetime, timedelta
 
def answerneiro(user_text):
    # Настройки
    start_date = datetime.strptime("02.09.2024", "%d.%m.%Y")  # Исправлено: datetime.strptime
    current_date = datetime.now()
    user_text = user_text.lower()  # Убрано input(), используется переданный user_text
    parsed_date = None

    # Мапа дней недели
    weekdays_map = {
        'понедельник': 0,
        'вторник': 1,
        'среда': 2,
        'четверг': 3,
        'пятница': 4,
        'суббота': 5,
        'воскресенье': 6
    }

    # Обработка ключевых слов вручную
    if "послезавтра" in user_text:
        parsed_date = current_date + timedelta(days=2)
    elif "завтра" in user_text:
        parsed_date = current_date + timedelta(days=1)
    elif "сегодня" in user_text:
        parsed_date = current_date
    elif "вчера" in user_text:
        parsed_date = current_date - timedelta(days=1)

    # Обработка "на этой/следующей/прошлой неделе"
    elif "следующ" in user_text and "недел" in user_text:
        parsed_date = current_date + timedelta(days=7)
    elif "на этой неделе" in user_text or "в эту неделю" in user_text:
        parsed_date = current_date
    elif "прошл" in user_text and "недел" in user_text:
        parsed_date = current_date - timedelta(days=7)

    # Обработка дней недели (включая "на следующую среду", "в прошлую пятницу")
    if not parsed_date:
        for day_str, target_weekday in weekdays_map.items():
            if day_str in user_text:
                # Определяем смещение
                current_weekday = current_date.weekday()
                if "следующ" in user_text:
                    days_ahead = (target_weekday - current_weekday + 7) % 7 + 7
                elif "прошл" in user_text:
                    days_behind = (current_weekday - target_weekday + 7) % 7
                    parsed_date = current_date - datetime.timedelta(days=days_behind or 7)
                    break
                else:
                    days_ahead = (target_weekday - current_weekday + 7) % 7
                    if days_ahead == 0:
                        days_ahead = 7
                parsed_date = current_date + datetime.timedelta(days=days_ahead)
                break

    # Попытка парсить обычную дату (12 июня, 10.06.2025 и т.п.)
    if not parsed_date:
        parsed_date = dateparser.parse(
            user_text,
            settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': current_date},
            languages=['ru']
        )

    # Ручной поиск даты, если dateparser не справился
    if not parsed_date:
        date_patterns = [
            r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b",
            r"\b\d{1,2}\s+[а-яё]+(?:\s+\d{4})?\b"
        ]
        for pattern in date_patterns:
            match = re.search(pattern, user_text)
            if match:
                parsed_date = dateparser.parse(
                    match.group(),
                    settings={'PREFER_DATES_FROM': 'future'},
                    languages=['ru']
                )
                break
    # Заданная дата начала (02.09.2024)
    start_date = datetime.strptime("02.09.2024", "%d.%m.%Y")

    # Текущая дата
    current_date = datetime.now()

    # Разница между текущей датой и заданной
    delta = current_date - start_date

    # Номер недели
    week_number1 = delta.days // 7   # Плюс 1, чтобы отсчитать с первой недели
    print(week_number1)
    
    # Вывод
    if parsed_date:
        delta = parsed_date - start_date
        week_number = delta.days // 7  
        print(f"📅 Дата: {parsed_date.strftime('%d.%m.%Y')}")
        print(f"🔢 Номер учебной недели: {week_number}")
    else:
        week_number=week_number1
        print(f"🔢 Номер учебной недели: {week_number}")

    



    # Чтение текста из файла
    with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{week_number}/allweek.txt", "r", encoding="utf-8") as file:
        text1 = file.read()
    with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{week_number+1}/allweek.txt", "r", encoding="utf-8") as file:
        text2 = file.read()
    with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{week_number-1}/allweek.txt", "r", encoding="utf-8") as file:
        text3 = file.read()
    text = text3+text1+text2 

    # Ввод вопроса
    question = user_text
    additional_prompt = (
        f"{text} Ты находишься в телеграм боте, если тебя пользователь спросит про пары и расписания то пользуйся информацией ранее слева, если что сейчас  {current_date }"
    )
    
    # Используем g4f для генерации ответа
    response = ChatCompletion.create(
        model="gpt-4",  # Выберите нужную модель, например, GPT-4
        messages=[
            {"role": "system", "content": additional_prompt},
            {"role": "user", "content": f"Текст: {text} \nВопрос: {question}"}
        ]
    )

    # Печать ответа
    print(f"Ответ от модели: {response}")
    return response
