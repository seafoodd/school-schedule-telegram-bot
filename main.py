import logging
from apscheduler.triggers.date import DateTrigger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
import asyncio
import json
from typing import Dict, List, Optional, Literal
from dotenv import load_dotenv
import os

global_loop: asyncio.AbstractEventLoop | None = None

lesson_start_times = [
    "7:30", "08:20", "09:10", "10:10", "11:00", "11:50", "12:40", "13:55",
    "14:45", "15:35", "16:35", "17:25", "18:15", "19:05",
]

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_DATE = date(2025, 6, 16)

logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()


def get_shift_type() -> Literal[1, 2]:
    today = date.today()
    weeks_passed = (today - BASE_DATE).days // 7
    return 1 if weeks_passed % 2 == 0 else 2

async def send_lesson(application, lesson) -> None:
    subject = lesson["subject"]
    time = lesson["time"]
    link = lesson["link"]
    await application.bot.send_message(chat_id=CHAT_ID, text=f"⏰ {subject} начинается в {time}\n🔗 {link}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"{update.effective_chat.id}")

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shift = get_shift_type()
    await update.message.reply_text(f"📅 Сейчас {'первая' if shift == 1 else 'вторая'} смена.")

def send_lesson_job(application, lesson) -> None:
    print(CHAT_ID)
    asyncio.run_coroutine_threadsafe(send_lesson(application, lesson), global_loop)

def setup_schedule(application, schedule) -> None:
    shift = get_shift_type()
    links = load_from_json("data/links.json")

    for lesson in schedule:
        lesson_day = lesson["day"]
        lesson_number = lesson["lesson_number"]

        if shift == 1:
            time_index = lesson_number - 1
        else:
            time_index = 13 - (lesson_number - 1)

        if time_index >= len(lesson_start_times):
            print(f"Warning: lesson_number {lesson_number} exceeds available start times")
            continue

        lesson_time = lesson_start_times[time_index]
        hour, minute = map(int, lesson_start_times[time_index].split(":"))
        lesson["link"] = links[lesson["subject"]]
        lesson["time"] = lesson_time

        now = datetime.now()
        days_ahead = lesson_day - now.weekday()
        if days_ahead < 0 or (days_ahead == 0 and (now.hour, now.minute) >= (hour, minute)):
            days_ahead += 7
        target_date = now + timedelta(days=days_ahead)
        target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

        scheduler.add_job(
            send_lesson_job,
            trigger='cron',
            day_of_week=lesson_day,
            hour=hour,
            minute=minute,
            args=[application, lesson],
            timezone='Europe/Belgrade'
        )

        print(f"{lesson_day+1}, {lesson_time}, {lesson['subject']}, {lesson['link']}")

def load_from_json(file_path) -> Dict[str, List[Optional[str]]]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    global global_loop

    raw_schedule = load_from_json("data/schedule.json")
    schedule = []
    for day, lessons in raw_schedule.items():
        for i, subject in enumerate(lessons):
            if subject:
                schedule.append({
                    "day": int(day),
                    "lesson_number": i + 1,
                    "subject": subject
                })

    application = Application.builder().token(TOKEN).build()
    global_loop = asyncio.get_event_loop()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("week", week))

    setup_schedule(application, schedule)
    scheduler.start()

    application.run_polling()

if __name__ == '__main__':
    main()
