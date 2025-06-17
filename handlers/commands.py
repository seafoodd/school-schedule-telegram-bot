from telegram import Update
from telegram.ext import ContextTypes
from services.scheduler import ScheduleService

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Chat ID: {update.effective_chat.id}")

async def week(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    schedule_service = ScheduleService()
    shift = schedule_service.get_shift_type()
    await update.message.reply_text(f"📅 Сейчас {'первая' if shift == 1 else 'вторая'} смена.")