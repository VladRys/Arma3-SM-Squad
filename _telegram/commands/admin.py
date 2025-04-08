
from telebot import types as t
from core.config import ADMINS

class AdminPanel():

    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, user_id, message):
        if str(user_id) in ADMINS:
            print(user_id)
            return True
        else:
            print(user_id)
            self.bot.send_message(message.chat.id, "Ты не являешься админом, чорт ебучий!")
            return False

    def admin_menu(self,message):
        admin_markup = t.InlineKeyboardMarkup(row_width=2)

        admin_markup.add(t.InlineKeyboardButton("Обновить ссылку на расписание", callback_data="update_parse_link"))
        admin_markup.add(t.InlineKeyboardButton("Обновить слоты (Ручной ввод)", callback_data="update_slots_manually"))

        user_id = message.from_user.id
        if self.is_admin(user_id, message):
            self.bot.send_message(message.chat.id, "Админ панель", reply_markup = admin_markup)


    def get_link(self, message):
        self.bot.send_message(message.chat.id, "Введи актуальную ссылку")
        self.bot.register_next_step_handler(message, self.save_link)

    def save_link(self, message):
        link = message.text
        print(link)
        
        try:
            with open("parser/link.txt", "w") as link_file:
                link_file.write(link)
            self.bot.send_message(message.chat.id, f"Ссылка: {link} была успешно сохранена")
        except FileNotFoundError:
            self.bot.send_message(message.chat.id, "Json файл не был найден!")
            print("[JSON ERROR] Json file not found")
        except Exception as e:
            self.bot.send_message(message.chat.id, "Ошибка", e)