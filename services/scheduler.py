from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List, Dict
from models.schedule import Lesson, ShiftType
from config.settings import settings
from services.schedule_loader import load_links
import logging

class ScheduleService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._started = False

    def start(self):
        if not self._started:
            self.scheduler.start()
            self._started = True
            logging.info("Scheduler started")
        else:
            logging.warning("Scheduler already running")

    @staticmethod
    def get_shift_type() -> ShiftType:
        today = date.today()
        base_date = date(*settings.BASE_DATE)
        weeks_passed = (today - base_date).days // 7
        return 1 if weeks_passed % 2 == 0 else 2

    def setup_lessons(self, application, lessons: List[Lesson], send_lesson_callback):
        shift = self.get_shift_type()
        links = load_links()

        for lesson in lessons:
            self._schedule_lesson(lesson, shift, links, application, send_lesson_callback)

    def _schedule_lesson(self, lesson: Lesson, shift: ShiftType, links: Dict[str, str],
                         application, callback):
        lesson_number = lesson["lesson_number"]

        if shift == 1:
            time_index = lesson_number - 1
        else:
            time_index = 13 - (lesson_number - 1)

        if time_index >= len(settings.LESSON_START_TIMES):
            logging.warning(f"Lesson number {lesson_number} exceeds available start times")
            return

        lesson_time = settings.LESSON_START_TIMES[time_index]
        hour, minute = map(int, lesson_time.split(":"))
        lesson["link"] = links[lesson["subject"]]
        lesson["time"] = lesson_time

        self.scheduler.add_job(
            callback,
            trigger='cron',
            day_of_week=lesson["day"],
            hour=hour,
            minute=minute,
            args=[application, lesson],
            timezone=settings.TIMEZONE
        )

        logging.info(f"Scheduled: Day {lesson['day'] + 1}, {lesson_time}, {lesson['subject']}")