from telegram import Update
from telegram.ext import ContextTypes
from services.scheduler import ScheduleService


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_msg = (
        "⚡ <b>Доступные команды:</b>\n"
        "/start - Показать это приветственное сообщение\n"
        "/week - Проверить текущую неделю (1-я/2-я)\n"
        "/chat_id - Показать ID чата\n"
        "/help - Показать список команд\n\n"
    )

    await update.message.reply_html(
        text=welcome_msg.format(chat_id=update.effective_chat.id),
        disable_web_page_preview=True
    )

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
        "/chat_id - Показать ID чата\n"
        "/help - Показать список команд\n\n"
        "🔧 <u>Решение проблем</u>:\n"
        "• Если что-то сломалось - @seafood_dev"
    )
    await update.message.reply_html(help_text)