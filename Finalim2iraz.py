from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from G4FGPT import answerneiro
import datetime
import asyncio
import time
# Токен бота
reminder_task = None
schedule_task = None
TOKEN = " "
# await reply_text("Все раздуплился")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем клавиатуру с командами
    welcome_message = (
        "Привет! 👋 Я бот для работы с расписанием.\n"
        "Выбери действие из меню ниже:"
    )
    keyboard = [
        ["👈Прошлый день","Расписание на сегодня","Следующий день👉"],  # Первый ряд кнопок
        ["⬅️Прошлая неделя","Расписание на эту неделю","Следующая неделя➡️"],
        ["Напоминалка","Инструкция","Проверка расписания"],
        ["Отмена напоминалки"," ","Отмена проверки расписание"]
                        # Второй ряд кнопок
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    today = datetime.date.today()
    day_number1 = today.isoweekday()
    day_number=day_number1
    
    with open("C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайты/current.txt", "r", encoding="utf-8") as cur:
        nWeek1=int(cur.read())

        nWeek=nWeek1
        nDWeek=nWeek
    if "day_number" not in context.user_data or "nDWeek" not in context.user_data:
        context.user_data["day_number"] = day_number1
        context.user_data["nDWeek"] = nWeek1
    day_number = context.user_data["day_number"]
    nDWeek = context.user_data["nDWeek"]
    
    with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nWeek1}/allweek.txt", "r", encoding="utf-8") as file:
        week=file.read()
    
    if "week" not in context.user_data:
        context.user_data["week"] = nWeek
    
    nWeek = context.user_data["week"]
    user_text = update.message.text
    print(user_text)
    if "Привет" in user_text:
        await update.message.reply_text("че")
    if user_text == "👈Прошлый день":
        
        day_number -= 1
        if day_number < 1:
            day_number = 7
            nDWeek -= 1
        context.user_data["day_number"] = day_number
        context.user_data["nDWeek"] = nDWeek
        if day_number == 7:
            await update.message.reply_text("отдыхаем")
         
        if day_number != 7:     
            with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nDWeek}/{day_number}.txt", "r", encoding="utf-8") as file:
                day = file.read()
            await update.message.reply_text(day)
    elif user_text == "Расписание на сегодня":
        context.user_data["day_number"] = day_number1
        context.user_data["nDWeek"]= nWeek1
        nDWeek==nWeek1
        if day_number1 == 7:
            await update.message.reply_text("отдыхаем")
        if day_number != 7:     
            with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nDWeek}/{day_number1}.txt", "r", encoding="utf-8") as f:
                    day_schedule = f.read()
            await update.message.reply_text(day_schedule)

    elif user_text == "Следующий день👉":
        
        day_number += 1
        if day_number > 8:
            day_number = 1
            nDWeek += 1
        context.user_data["day_number"] = day_number
        context.user_data["nDWeek"] = nDWeek
        if day_number == 7:
            await update.message.reply_text("отдыхаем")
         
        if day_number < 7:     
            with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nDWeek}/{day_number}.txt", "r", encoding="utf-8") as file:
                day = file.read()
            await update.message.reply_text(day)
    elif user_text == "Отмена напоминалки":
        global reminder_task
        if reminder_task and not reminder_task.done():
            reminder_task.cancel()
            reminder_task = None
            await update.message.reply_text("❌ Напоминалка отменена.")
        else:
            await update.message.reply_text("ℹ️ Активных напоминалок нет.")

    elif user_text == "Отмена проверки расписание":
        global schedule_task
        if schedule_task and not schedule_task.done():
            schedule_task.cancel()
            schedule_task = None
            await update.message.reply_text("❌ Автопроверка расписания остановлена.")
        else:
            await update.message.reply_text("ℹ️ Автопроверка не запущена.")
        

    elif user_text == "⬅️Прошлая неделя":
        
        nWeek-=1
        context.user_data["week"] = nWeek
        nWeek = context.user_data["week"]
        if nWeek < 52 and nWeek > -1:
            with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nWeek}/allweek.txt", "r", encoding="utf-8") as file:
                week1=file.read()
        await update.message.reply_text(week1)

    elif user_text == "Расписание на эту неделю":
        context.user_data["week"]=nWeek1
        nWeek=nWeek1
        with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nWeek1}/allweek.txt", "r", encoding="utf-8") as file:
            week1=file.read()
        await update.message.reply_text(week1)

    elif user_text == "Следующая неделя➡️":

            
        nWeek+=1
        context.user_data["week"] = nWeek
        nWeek = context.user_data["week"]
        if nWeek < 52 and nWeek > -1:
            with open(f"C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/{nWeek}/allweek.txt", "r", encoding="utf-8") as file:
                week1=file.read()
        await update.message.reply_text(week1)
    elif user_text == "Напоминалка":
        await update.message.reply_text("✍️ Напиши текст для напоминания")
        context.user_data["wait_reminder_text"] = True
        return

    elif context.user_data.get("wait_reminder_text"):
        context.user_data["reminder_text"] = user_text
        context.user_data["wait_reminder_text"] = False
        context.user_data["wait_reminder_time"] = True
        await update.message.reply_text("⏰ Напиши время через пробел: дни часы минуты (например: 0 0 30 для 30 минут)")
        return

    elif context.user_data.get("wait_reminder_time"):
        context.user_data["wait_reminder_time"] = False
        
        
        seconds = parse_time_to_seconds(user_text)

        if seconds == 0:
            await update.message.reply_text("⛔ Неправильный формат. Попробуй снова.")
            return
        reminder_text = context.user_data["reminder_text"]
        days, hours, minutes = map(int, user_text.strip().split())
        await update.message.reply_text(f"✅ Напомню через {days} дней {hours} часов {minutes} минут!")
         
        reminder_task = asyncio.create_task(timer(update, context, reminder_text, seconds))
        return
        
    elif user_text == "Инструкция":
        instruction_keyboard = [
            ["📅 Навигация по расписанию", "⏰ Напоминалка"],
            ["🤖 Разговор с ботом","о боте"],
            ["🔙 Назад в меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(instruction_keyboard, resize_keyboard=True)
        await update.message.reply_text("📘 Выбери раздел инструкции:", reply_markup=reply_markup)
    elif user_text == "📅 Навигация по расписанию":
        nav_text = (
            "📅 *Навигация по расписанию и неделям:*\n\n"
            "🔸 *Прошлый день / Следующий день* — переход по дням недели.\n"
            "🔸 *Расписание на сегодня* — сбрасывает переход и показывает текущий день.\n\n"
            "🔸 *Прошлая неделя / Следующая неделя* — показывает полное расписание на нужную неделю.\n"
            "🔸 *Расписание на эту неделю* — сбрасывает на текущую неделю.\n\n"
            "_Если день = воскресенье (7), бот напишет «отдыхаем»._"
        )
        await update.message.reply_text(nav_text, parse_mode="Markdown")
    elif user_text == "о боте":
        reminder_text = ("Бот расписание университета ТПУ, группы 8В24")
        await update.message.reply_text(reminder_text, parse_mode="Markdown")
    elif user_text == "⏰ Напоминалка":
        reminder_text = (
            "⏰ *Как поставить напоминание:*\n\n"
            "1. Нажми *«Напоминалка»* в главном меню.\n"
            "2. Напиши текст, о чём напомнить.\n"
            "3. Введи время через пробел: *дни часы минуты* (например: `0 0 30`).\n\n"
            "✅ Бот напомнит в нужное время.\n"
            "❌ Чтобы отменить — нажми *«Отмена напоминалки»*."
        )
        await update.message.reply_text(reminder_text, parse_mode="Markdown")

    elif user_text == "🤖 Разговор с ботом":
        chat_text = (
            "🤖 *Разговор с ботом:*\n\n"
            "Если хочешь пообщаться — напиши сообщение, начиная с:\n"
            "`Нейронка, `\n\n"
            "Например: `Нейронка, расскажи анекдот`\n"
            "или `Нейронка, какое расписание на пятницу следующей недели?`\n\n"
            "📌 Бот ответит тебе в стиле ИИ и знает расписание на:\n"
            "• прошлую неделю\n"
            "• текущую неделю\n"
            "• следующую неделю\n\n"
            "Так что ты можешь спрашивать у него расписание в свободной форме!")
        await update.message.reply_text(chat_text, parse_mode="Markdown")


    elif user_text == "🔙 Назад в меню":
        main_keyboard = [
            ["👈Прошлый день","Расписание на сегодня","Следующий день👉"],  # Первый ряд кнопок
            ["⬅️Прошлая неделя","Расписание на эту неделю","Следующая неделя➡️"],
            ["Напоминалка","Инструкция","Проверка расписания"],
            ["Отмена напоминалки"," ","Отмена проверки расписание"]
        ]
        reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        await update.message.reply_text("🔙 Главное меню:", reply_markup=reply_markup)

    elif user_text == "Проверка расписания":
         
        schedule_task = asyncio.create_task(checkIZM(update, context)) 
     
    if "Нейронка," in user_text:
         response = answerneiro(user_text)
         await update.message.reply_text(response)
async def timer(update: Update, context: ContextTypes.DEFAULT_TYPE, reminder_text: str, delay_seconds: int):
    await asyncio.sleep(delay_seconds)
    await update.message.reply_text(f"🔔 Напоминание: {reminder_text}")
async def checkIZM(update: Update, context: ContextTypes.DEFAULT_TYPE):
    while True:
        with open("C:/Users/vladi/OneDrive/Документы/pyton/tg botara/сайтыобработка/peremena.txt", "r", encoding="utf-8") as per:
            FT=str(per.read())
        try:
            # Здесь вызывается проверка расписания
            if FT == "false":
                await update.message.reply_text("В расписание измнений нету")
            else:
                await update.message.reply_text("РАСПИСАНИЕ ПОМЕНЯЛОСЬ")
        except Exception as e:
            print(f"Ошибка при проверке расписания")

        await asyncio.sleep(6 * 60 * 60)  # ждать 6 часов
def parse_time_to_seconds(time_str: str) -> int:
    try:
        parts = list(map(int, time_str.strip().split()))
        if len(parts) != 3:
            return 0
        days, hours, minutes = parts
        total_seconds = days * 86400 + hours * 3600 + minutes * 60
        return total_seconds
    except ValueError:
        return 0
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("start", start))    
    app.run_polling()
print("Бот запущен...")
if __name__ == "__main__":
    main()