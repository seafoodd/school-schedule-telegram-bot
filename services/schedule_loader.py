import json
from pathlib import Path
from typing import Dict, List
from models.schedule import Lesson


def load_from_json(file_path: str) -> Dict:
    with open(Path(__file__).parent.parent / file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_schedule() -> List[Lesson]:
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

    return schedule


def load_links() -> Dict[str, str]:
    return load_from_json("data/links.json")