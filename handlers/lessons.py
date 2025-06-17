import logging

from telegram.ext import Application

from config.settings import settings
from models.schedule import Lesson


async def send_lesson_notification(application: Application, lesson: Lesson) -> None:
    try:
        subjects = lesson['subject'].split('/')
        if len(subjects) > 1:
            links = [
                f'<a href="{settings.links[subj]}">{subj}</a>'
                for subj in subjects
            ]
            text = f"⏰ <b>{links[0]}/{links[1]}</b> начинаются в <b>{lesson['time']}</b>"
        else:
            subj = subjects[0]
            link = f'<a href="{settings.links[subj]}">{subj}</a>'
            text = f"⏰ {link} начинается в {lesson['time']}"

        await application.bot.send_message(
            chat_id=settings.CHAT_ID,
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"Failed to send lesson notification: {e}")
