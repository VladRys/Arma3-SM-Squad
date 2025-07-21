import json

from parser.parser import Parser, SiteParser, StatParser, StatMissionsParser, StatFormatter, MissionDownloader

from telebot import types as t

from telegram.commands.admin import AdminPanel
from core.config import *

from telegram.utils.keyboards import CustomInlineKeyboards
from telegram.utils.donate import Donate

from logs.setup_logs import setup_logger, unload_error_logs, unload_logs


class Handlers():
    def __init__(self, bot, database):
        self.bot = bot
        self.db = database
        self.donate = Donate(self.bot)
        self.custom_markups = CustomInlineKeyboards(self.bot)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)
        
        self.l = setup_logger()

        self.parser = Parser(SiteParser, StatParser, StatMissionsParser, StatFormatter)
        

        self.user_state = {}


        self.bot.message_handler(func=lambda m: self.user_state.get(m.from_user.id) == 'waiting_json', content_types=['document'])(self.handle_json)
        
        self.admin_panel = AdminPanel(self.bot)

    def callback_query(self, call):
        if call.data == "unload_logs":
            unload_error_logs(self.bot, call.message)
            unload_logs(self.bot, call.message)
            

        if call.data == "download_missions":
            parsed_data = self.parser.parse_missions()
            text = ""
            x, y = 0, 0
            while x < 4 and y < 7:
                text += f"*{TVT_DATES[x]}*\n - [Первая]({parsed_data['MISSION_LINKS'][y]})\n - [Вторая]({parsed_data['MISSION_LINKS'][y+1]})\n\n"
                x += 1
                y += 2

            self.bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

        # === Stats ===
        if call.data == "top_mission_squadstat":
            with open("parser/ocap_missions/active_mission.txt", "r", encoding="utf-8") as f:
                mission_link = f.read().strip()

            msg = self.bot.send_message(
                chat_id=call.message.chat.id,
                text="Получение статистики отряда...",
                parse_mode="Markdown"
            )
            stat = self.parser.stats.missions_stats.smersh_top_mission_stat(mission_link)
            
            self.bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                text=f"\n\nSMERSH STAT\n\n{stat}"
            )

            text = f"{call.message.text}\n\n*SMERSH STAT*\n\n{stat}"

            # Клавиатура отряда
            self.bot.edit_message_reply_markup(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                reply_markup=self.custom_markups.hide_squad_markup(call.message.message_id)
            )

            # Клавиатура общей статы
            self.bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None
            )

        if call.data.startswith("hide_squad_stat_"):
            self.bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )

            msg_id = call.data.split("_")[-1]
            self.bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = msg_id, reply_markup = self.custom_markups.top_mission_markup()) 
            

        # === Admin callbacks ===
        if call.data == "update_parse_link":
            self.admin_panel.get_link(call.message)
        
        if call.data == "update_slots_json":
            self.user_state[call.from_user.id] = 'waiting_json'
            msg = self.bot.send_message(call.message.chat.id, 'Отправь json слотов', parse_mode='Markdown')

        self.bot.answer_callback_query(call.id)

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
                self.custom_makups.get_error_markup(message.chat.id, 'Ошибка во время получения JSON слотов. Посмотреть ошибку детальнее можно выгрузив логи.')
                self.l.error(f"[ERROR] while handling new json: {e}")
            except json.JSONDecodeError:
                self.bot.reply_to(message, "Неверный JSON файл. Предыдущий был заменен на поврежденный/нечитаемый.")
                self.l.error("[ERROR] Json file was corrupted and changed by previous")
        else:
            return