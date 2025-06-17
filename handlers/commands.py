from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.settings import settings
from models.schedule import Lesson
from services.scheduler import ScheduleService
from typing import List
from datetime import datetime

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_msg = (
        "⚡ <b>Доступные команды:</b>\n"
        "/start - Показать это приветственное сообщение\n"
        "/week - Проверить текущую неделю (1-я/2-я)\n"
        "/schedule - Показать расписание\n"
        "/chat_id - Показать ID чата\n"
        "/help - Показать список команд\n\n"
    )

    await update.message.reply_html(
        text=welcome_msg.format(chat_id=update.effective_chat.id),
        disable_web_page_preview=True
    )


async def schedule_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Сегодня", callback_data="schedule_today"),
         InlineKeyboardButton("Неделя", callback_data="schedule_week")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📅 Выберите расписание:",
        reply_markup=reply_markup
    )


async def schedule_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    today = datetime.now().weekday()
    schedule_service = ScheduleService()
    shift = schedule_service.get_shift_type()

    if "today" in query.data:
        today_lessons = [l for l in settings.schedule if l["day"] == today]
        message = format_daily_schedule(today_lessons, shift, today)
    else:
        message = format_weekly_schedule(shift)

    await query.edit_message_text(
        text=message,
        parse_mode="HTML"
    )


def format_daily_schedule(lessons: List[Lesson], shift: int, day: int) -> str:
    day_names = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]
    message = [f"<b>📅 Расписание на {day_names[day]} ({shift} смена)</b>\n"]

    for lesson in sorted(lessons, key=lambda x: x["lesson_number"]):
        time_index = (lesson["lesson_number"] - 1) if shift == 1 else (13 - lesson["lesson_number"])
        if time_index < len(settings.LESSON_START_TIMES):
            start_time = settings.LESSON_START_TIMES[time_index]
            hour, minute = map(int, start_time.split(':'))
            end_time = f"{(hour + (minute + 45) // 60):02d}:{(minute + 45) % 60:02d}"

            current_time = datetime.now().time()
            current_minutes = current_time.hour * 60 + current_time.minute
            lesson_start_minutes = hour * 60 + minute
            lesson_end_minutes = lesson_start_minutes + settings.LESSON_DURATION

            is_ongoing = lesson_start_minutes <= current_minutes < lesson_end_minutes
            is_finished = current_minutes >= lesson_end_minutes
            is_upcoming = current_minutes < lesson_start_minutes

            status_icon = "🟡" if is_upcoming else "🔴" if is_ongoing else "🟢"
            strikethrough = "<s>" if is_finished else ""
            time_display = f"{start_time}-{end_time}"
            link = f' (<a href="{settings.links[lesson['subject']]}">идёт сейчас</a>)' if is_ongoing else ""

            message.append(
                f"{status_icon} {strikethrough}{time_display}: <b>{lesson['subject']}</b>{'</s>' if is_finished else ''}"
                f"{link if is_ongoing else ''}"
            )

    return "\n".join(message) if len(message) > 1 else "Сегодня нет уроков"


def format_weekly_schedule(shift: int) -> str:
    day_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    message = [f"<b>📅 Расписание на неделю ({shift} смена)</b>"]

    by_day = {day: [] for day in range(7)}
    for lesson in settings.schedule:
        by_day[lesson["day"]].append(lesson)

    for day in range(7):
        day_lessons = sorted(by_day[day], key=lambda x: x["lesson_number"])
        if not day_lessons:
            continue

        day_msg = [f"\n<b>{day_names[day]}:</b>"]
        for lesson in day_lessons:
            time_index = (lesson["lesson_number"] - 1) if shift == 1 else (13 - lesson["lesson_number"])
            if time_index < len(settings.LESSON_START_TIMES):
                start_time = settings.LESSON_START_TIMES[time_index]
                day_msg.append(f"  {start_time}: {lesson['subject']}")

        message.append("\n".join(day_msg))

    return "\n".join(message) if len(message) > 1 else "No lessons scheduled this week"

async def chat_id(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id_message = (
        "📝 <i>Chat ID:</i> <code>{chat_id}</code>"
    )

    await update.message.reply_html(
        text=chat_id_message.format(chat_id=update.effective_chat.id),
        disable_web_page_preview=True
    )

async def week(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    schedule_service = ScheduleService()
    shift = schedule_service.get_shift_type()
    await update.message.reply_text(f"📅 Сейчас {'первая' if shift == 1 else 'вторая'} смена.")

async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🆘 <b>Помощь по боту</b>\n\n"
        "📌 <u>Основные команды</u>:\n"
        "/start - Показать приветственное сообщение\n"
        "/week - Проверить текущую неделю (1-я/2-я)\n"
        "/schedule - Показать расписание\n"
        "/chat_id - Показать ID чата\n"
        "/help - Показать список команд\n\n"
        "🔧 <u>Решение проблем</u>:\n"
        "• Если что-то сломалось - @seafood_dev"
    )
    await update.message.reply_html(help_text)