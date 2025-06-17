from typing import TypedDict, Literal, Optional

class Lesson(TypedDict):
    day: int
    lesson_number: int
    subject: str
    time: Optional[str]
    link: Optional[str]

ShiftType = Literal[1, 2]