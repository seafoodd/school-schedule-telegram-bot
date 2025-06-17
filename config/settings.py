import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class Settings:
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    BASE_DATE = (2025, 6, 16)  # year/month/day
    TIMEZONE = 'Europe/Belgrade'

    LESSON_START_TIMES = [
        "7:30", "08:20", "09:10", "10:10", "11:00", "11:50", "12:40", "13:55",
        "14:45", "15:35", "16:35", "17:25", "18:15", "19:05",
    ]


settings = Settings()