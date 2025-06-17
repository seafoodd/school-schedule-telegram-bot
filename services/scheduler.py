from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from typing import List, Dict
from models.schedule import Lesson, ShiftType
from config.settings import settings
from services.schedule_loader import load_links
import logging
from datetime import datetime, timedelta
from copy import deepcopy

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
        links = load_links()

        for lesson in lessons:
            self._schedule_lesson(lesson, links, application, send_lesson_callback)

    def _schedule_lesson(self, lesson: Lesson, links: Dict[str, str],
                         application, callback):
        lesson_number = lesson["lesson_number"]

        first_shift_index = lesson_number - 1
        second_shift_index = 13 - (lesson_number - 1)

        if first_shift_index >= len(settings.LESSON_START_TIMES) or \
                second_shift_index >= len(settings.LESSON_START_TIMES):
            logging.warning(f"Lesson number {lesson_number} exceeds available start times")
            return

        base_dt = datetime(*settings.BASE_DATE)

        lesson1 = deepcopy(lesson)
        lesson1["link"] = links[lesson["subject"]]
        lesson1["time"] = settings.LESSON_START_TIMES[first_shift_index]
        hour, minute = map(int, lesson1["time"].split(":"))

        self.scheduler.add_job(
            callback,
            trigger='cron',
            day_of_week=lesson["day"],
            hour=hour,
            minute=minute,
            args=[application, lesson1],
            timezone=settings.TIMEZONE,
            week='1-53/2',  # Odd weeks
            start_date=base_dt
        )

        lesson2 = deepcopy(lesson)
        lesson2["link"] = links[lesson["subject"]]
        lesson2["time"] = settings.LESSON_START_TIMES[second_shift_index]
        hour, minute = map(int, lesson2["time"].split(":"))

        self.scheduler.add_job(
            callback,
            trigger='cron',
            day_of_week=lesson["day"],
            hour=hour,
            minute=minute,
            args=[application, lesson2],
            timezone=settings.TIMEZONE,
            week='2-52/2',  # Even weeks
            start_date=base_dt + timedelta(weeks=1)
        )

        logging.info(f"Scheduled both shifts for {lesson['subject']}: "
                     f"1st shift at {lesson1['time']} (odd weeks), "
                     f"2nd shift at {lesson2['time']} (even weeks)")