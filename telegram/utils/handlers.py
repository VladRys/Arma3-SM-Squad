import json

from parser.parser import parse_missions

from telegram.commands.admin import AdminPanel
from core.config import SLOTS_FILE_PATH, TVT_DATES

class Handlers():
    def __init__(self, bot, database):
        self.bot = bot
        self.db = database
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)
        self.bot.message_handler(content_types=["document"])(self.handle_json)
        self.admin_panel = AdminPanel(self.bot)

    def callback_query(self, call):
        if call.data == "download_missions":
            parsed_data = parse_missions()
            text = ""
            x, y = 0, 0
            while x < 4 and y < 7:
                text += f"*{TVT_DATES[x]}*\n - [Первая]({parsed_data['MISSION_LINKS'][y]})\n - [Вторая]({parsed_data['MISSION_LINKS'][y+1]})\n\n"
                x += 1
                y += 2

            self.bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

    
        # Admin
        if call.data == "update_parse_link":
            self.admin_panel.get_link(call.message)
        
        self.bot.answer_callback_query(call.id)

    def handle_json(self, message):
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
        except json.JSONDecodeError:
            self.bot.reply_to(message, "Неверный JSON файл. Предыдущий был заменен на поврежденный/нечитаемый.")