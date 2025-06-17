import logging

from telegram.ext import Application

from config.settings import settings
from models.schedule import Lesson


async def send_lesson_notification(application: Application, lesson: Lesson) -> None:
    try:
        subjects = lesson['subject'].split('/')
        links = [
            f'<a href="{lesson['link'][i]}">{subjects[i]}</a>'
            for i in range(len(subjects))
        ]
        links = "/".join(links)

        text = f"⏰ <b>{links}</b> начина{'ю' if len(subjects) > 1 else 'е'}тся в <b>{lesson['time']}</b>"

        await application.bot.send_message(
            chat_id=settings.CHAT_ID,
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"Failed to send lesson notification: {e}")
