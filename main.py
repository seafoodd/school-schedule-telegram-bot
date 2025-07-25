import asyncio
import logging

from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from config.settings import settings
from handlers.commands import start, week, chat_id, help_command, schedule_command, schedule_callback
from handlers.lessons import send_lesson_notification
from services.scheduler import ScheduleService

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
        self.application.add_handler(CommandHandler("schedule", schedule_command))
        self.application.add_handler(CallbackQueryHandler(schedule_callback, pattern="^schedule_"))
        self.application.add_handler(CommandHandler("week", week))
        self.application.add_handler(CommandHandler("chat_id", chat_id))
        self.application.add_handler(CommandHandler("help", help_command))

    def setup_schedule(self):
        self.schedule_service.setup_lessons(
            self.application,
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

async def test_on_startup(application: Application):
    test_lessons = [{
        'day': 1,
        'lesson_number': 3,
        'subject': 'Test',
        'link': ['https://natribu.org/'],
        'time': '11:04'
    },{
        'day': 1,
        'lesson_number': 3,
        'subject': 'Test/Test2',
        'link': ['https://natribu.org/', 'https://naribu.org/'],
        'time': '11:04'
    }]
    for lesson in test_lessons:
        await send_lesson_notification(application, lesson)

if __name__ == '__main__':
    bot = TelegramBot()
    # bot.application.post_init = test_on_startup
    bot.run()
