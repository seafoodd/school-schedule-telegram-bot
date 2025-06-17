# 🏫 School Schedule Telegram Bot

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An automated bot that sends lesson notifications and shift schedules to students via Telegram.

## ✨ Features

- 📅 Automatic shift detection (odd/even weeks)
- ⏰ Lesson reminders with direct Zoom/Meet links
- 🔔 Customizable notification times
- 📱 Simple `/week` command to check current shift

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Telegram Bot Token ([get one from @BotFather](https://core.telegram.org/bots#6-botfather))

### Installation
```bash
# Clone the repository
git clone https://github.com/seafoodd/school-schedule-telegram-bot.git
cd school-schedule-telegram-bot

# Set up a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
```bash
cp .env.example .env  # On Windows: copy .env.example .env
```
2. Add your credentials:
```ini
TOKEN=YOUR-TOKEN            # From @BotFather
CHAT_ID=YOUR-GROUP-CHAT-ID  # Numeric chat ID
```

### Running the Bot
```bash
python main.py
```

## 🤖 Available Commands
| Command    | Description              |
|------------|--------------------------|
| `/start`   | Show the welcome message |
| `/chat_id` | Show group chat id       |
| `/week`    | Check current shift week |
| `/help`    | Show command list        |

## 📈 Advanced Setup
### Customizing Schedules and Links
Edit the JSON files in `data/` following this format:

##### schedule.json:
```json
{
  "1": ["Math", "Physics", null, "Chemistry"],
  "2": ["Literature", "Biology", "PE", null]
}
```
##### links.json:
```json
{
  "Psychology": "https://meet.google.com/xxx-xxxx-xxx",
  "English": "https://meet.google.com/xxx-xxxx-xxx"
}

```

## 📜 License
MIT © @seafoodd - See [LICENSE](LICENSE) for details
