import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List
import json

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class Settings:
    def __init__(self):
        self.TOKEN = os.getenv("TOKEN")
        self.CHAT_ID = os.getenv("CHAT_ID")
        self.BASE_DATE = (2025, 6, 16)
        self.TIMEZONE = 'Europe/Belgrade'
        self.LESSON_DURATION = 45
        self._links = None
        self._schedule = None

        self.LESSON_START_TIMES = [
            "07:30", "08:20", "09:10", "10:10", "11:00", "11:50", "12:40", "13:55",
            "14:45", "15:35", "16:35", "17:25", "18:15", "19:05",
        ]

    @property
    def links(self) -> Dict[str, str]:
        if self._links is None:
            self._links = self._load_json("data/links.json")
        return self._links

    @property
    def schedule(self) -> List[Dict]:
        if self._schedule is None:
            raw = self._load_json("data/schedule.json")
            self._schedule = self._process_schedule(raw)
        return self._schedule

    @staticmethod
    def _load_json(path: str) -> Dict:
        full_path = BASE_DIR / path
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load {path}: {str(e)}")

    @staticmethod
    def _process_schedule(raw_schedule: Dict) -> List[Dict]:
        processed = []
        for day, lessons in raw_schedule.items():
            for i, subject in enumerate(lessons):
                if subject:
                    processed.append({
                        "day": int(day),
                        "lesson_number": i + 1,
                        "subject": subject
                    })
        return processed

    def reload_data(self):
        self._links = None
        self._schedule = None


settings = Settings()