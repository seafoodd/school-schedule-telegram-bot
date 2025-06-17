import logging
from telegram.ext import Application
from models.schedule import Lesson
from config.settings import settings

async def send_lesson_notification(application: Application, lesson: Lesson) -> None:
    try:
        text = f"⏰ {lesson['subject']} начинается в {lesson['time']}\n🔗 {lesson['link']}"
        await application.bot.send_message(
            chat_id=settings.CHAT_ID,
            text=text
        )
    except Exception as e:
        logging.error(f"Failed to send lesson notification: {e}")