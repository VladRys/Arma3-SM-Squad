import telebot 

from core.config import TOKEN_TELEGAM as MAIN_TOKEN, TEST_TOKEN_TELEGRAM as TEST_TOKEN, TEST_MODE
from database.db import BotDB as Database
from _telegram.commands.slash_commands import SlashCommands
from _telegram.commands.admin import AdminPanel
from _telegram.utils.handlers import Handlers

TOKEN = TEST_TOKEN if TEST_MODE == 1 else MAIN_TOKEN

bot = telebot.TeleBot(TOKEN)

commands = SlashCommands(bot)
all_handlers = Handlers(bot, Database)
admin = AdminPanel(bot)
 
try:
    print("[+++] Telegram")
    bot.polling(TOKEN)
except Exception as e:
    print("[ERROR]", e)