import asyncio
import logging
from telegram.ext import Application, CommandHandler
from config.settings import settings
from services.scheduler import ScheduleService
from services.schedule_loader import load_schedule
from handlers.commands import start, week, chat_id, help_command
from handlers.lessons import send_lesson_notification

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.application = Application.builder().token(settings.TOKEN).build()
        self.schedule_service = ScheduleService()
        self.loop = asyncio.get_event_loop()

        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("week", week))
        self.application.add_handler(CommandHandler("chat_id", chat_id))
        self.application.add_handler(CommandHandler("help", help_command))

    def setup_schedule(self):
        schedule = load_schedule()
        self.schedule_service.setup_lessons(
            self.application,
            schedule,
            self._send_lesson_wrapper
        )

    def _send_lesson_wrapper(self, application, lesson):
        asyncio.run_coroutine_threadsafe(
            send_lesson_notification(application, lesson),
            self.loop
        )

    def run(self):
        self.setup_handlers()
        self.setup_schedule()
        self.schedule_service.start()
        self.application.run_polling()

        if not self.schedule_service.scheduler.running:
            self.schedule_service.start()

        self.application.run_polling(
            close_loop=False,
            stop_signals=None
        )


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()