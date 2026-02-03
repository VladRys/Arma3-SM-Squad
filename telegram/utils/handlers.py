import telebot
from telebot import types as t

from telegram.commands.admin import AdminPanel
from core.config import *
from telegram.utils.keyboards import CustomInlineKeyboards

from logs.setup_logs import setup_logger, unload_error_logs, unload_logs
from parser.parser import SolidGamesParser
from telegram.utils.utils import Formatter

class Handlers():
    def __init__(self, bot: telebot.TeleBot, parser: SolidGamesParser):
        self.bot = bot
        self.custom_markups = CustomInlineKeyboards(self.bot)
        self.l = setup_logger()

        self.parser = parser
 
        self.admin_panel = AdminPanel(self.bot)
    
        self._register_handlers(self.bot)
    def _register_handlers(self, bot):
        @bot.callback_query_handler(func=lambda call: call.data == "unload_logs")
        def unload_logs_callback(call: t.CallbackQuery):
            unload_error_logs(bot, call.message)
            unload_logs(bot, call.message)
            
            bot.answer_callback_query(call.id)

        @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("mission:"))
        def mission_callback(query):
            try:
                idx = int(query.data.split(":", 1)[1])
            except Exception:
                bot.send_message(query.message.chat.id, "Неверная кнопка")
                return

            latest = self.parser.parse_latest()
            if not latest:
                return

            missions = latest.get("missions", [])
            if idx < 0 or idx >= len(missions):
                bot.answer_callback_query(query.id, "Миссия недоступна", show_alert=True)
                return

            text = Formatter.format_mission(missions, idx, latest.get("title"))
            keyboard = self.custom_markups.missions_keyboard(idx)
            bot.edit_message_text(
                text,
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard
            )
            bot.answer_callback_query(query.id)
