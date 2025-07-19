import json

from parser.parser import Parser, SiteParser, StatParser, StatMissionsParser

from telebot import types as t

from telegram.commands.admin import AdminPanel
from core.config import *

from logs.setup_logs import setup_logger, unload_error_logs

class Handlers():
    def __init__(self, bot, database):
        self.bot = bot
        self.db = database
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)
        
        self.l = setup_logger()

        self.parser = Parser(SiteParser, StatParser, StatMissionsParser)

        self.user_state = {}

        self.bot.message_handler(func=lambda m: self.user_state.get(m.from_user.id) == 'waiting_json', content_types=['document'])(self.handle_json)
        
        self.admin_panel = AdminPanel(self.bot)

    def callback_query(self, call):
        if call.data == "unload_error_logs":
            unload_error_logs(self.bot, call.message)

        if call.data == "download_missions":
            parsed_data = self.parser.parse_missions()
            text = ""
            x, y = 0, 0
            while x < 4 and y < 7:
                text += f"*{TVT_DATES[x]}*\n - [Первая]({parsed_data['MISSION_LINKS'][y]})\n - [Вторая]({parsed_data['MISSION_LINKS'][y+1]})\n\n"
                x += 1
                y += 2

            self.bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

    
        # === Admin callbacks ===
        if call.data == "update_parse_link":
            self.admin_panel.get_link(call.message)
        
        if call.data == "update_slots_json":
            self.user_state[call.from_user.id] = 'waiting_json'
            msg = self.bot.send_message(call.message.chat.id, 'Отправь json слотов', parse_mode='Markdown')

        self.bot.answer_callback_query(call.id)


    # === Should has admin condition ===
    def handle_json(self, message):
        if message.from_user.id not in ADMINS:
            file_info = self.bot.get_file(message.document.file_id)

            if not message.document.file_name.endswith(".json"):
                self.bot.reply_to(message, "Отправленный файл не является JSON")
                return

            file_path = file_info.file_path
            downloaded_file = self.bot.download_file(file_path)

            with open(SLOTS_FILE_PATH, "wb") as file:
                file.write(downloaded_file)

            try:
                with open(SLOTS_FILE_PATH, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)

                    self.bot.send_message(message.chat.id, f"Новый JSON файл: \n\n{data}")
                    self.l.info("[JSON] New json file was saved!")
                    self.user_state[message.from_user.id] = None
            except Exception as e:
                error_markup = t.InlineKeyboardMarkup(row_width=1)
                error_markup.add(t.InlineKeyboardButton(text='🔨 Выгрузить логи', callback_data='unload_error_logs'))

                self.bot.send_message(message.chat.id, 'Ошибка во время получения JSON слотов. Посмотреть ошибку детальнее можно выгрузив логи.', parse_mode='Markdown')
                self.l.error(f"[ERROR] while handling new json: {e}")
            except json.JSONDecodeError:
                self.bot.reply_to(message, "Неверный JSON файл. Предыдущий был заменен на поврежденный/нечитаемый.")
                self.l.error("[ERROR] Json file was corrupted and changed by previous")
        else:
            return
        
    def commands_hanlder(self):
        pass