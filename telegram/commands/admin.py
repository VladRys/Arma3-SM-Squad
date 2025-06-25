
from telebot import types as t
from core.config import ADMINS

from logs.setup_logs import *
from telegram.utils.keyboards import CustomInlineKeyboards


class AdminPanel():

    def __init__(self, bot):
        self.bot = bot

        self.l = setup_logger()
        
        self.custom_markups = CustomInlineKeyboards(self.bot)

    def is_admin(self, user_id, message):
        if str(user_id) in ADMINS:
            return True
        else:
            self.bot.send_message(message.chat.id, "Ты не являешься админом, чорт ебучий!")
            return False

    def admin_menu(self,message):
        admin_markup = t.InlineKeyboardMarkup(row_width=2)

        admin_markup.add(t.InlineKeyboardButton("Обновить ссылку на расписание", callback_data="update_parse_link"))
        admin_markup.add(t.InlineKeyboardButton("Обновить слоты (JSON)", callback_data="update_slots_json"))
        admin_markup.add(t.InlineKeyboardButton(text='🔨 Выгрузить логи', callback_data='unload_error_logs'))
        user_id = message.from_user.id
        if self.is_admin(user_id, message):
            self.bot.send_message(message.chat.id, "Админ панель", reply_markup = admin_markup)


    def get_link(self, message):
        self.bot.send_message(message.chat.id, "Введи актуальную ссылку")
        self.bot.register_next_step_handler(message, self.save_link)

    def save_link(self, message):
        link = message.text
        
        try:
            with open("parser/link.txt", "w") as link_file:
                link_file.write(link)

            self.bot.send_message(message.chat.id, f"Ссылка: {link} была успешно сохранена")
            
            self.l.info(f"[LINK] Saved Link: {link}")
        except FileNotFoundError:
            self.custom_markups.get_error_markup(message.chat.id, "link.txt файл не был найден! Посмотреть ошибку детальнее можно выгрузив логи.")
            print("[LINK ERROR] Link txt file was not found")

        except Exception as e:
            self.custom_markups.get_error_markup(message.chat.id, 'Ошибка при сохранении ссылки расписания! Посмотреть ошибку детальнее можно выгрузив логи.')
            self.l.error(f"[LINK ERROR] {e}")