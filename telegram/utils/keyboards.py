from telebot import types as t
from core.config import SOLID_GAMES_URL

class CustomInlineKeyboards():
    def __init__(self, bot):
        self.bot = bot
        
    def get_error_markup(self, chat_id, message):
        error_markup = t.InlineKeyboardMarkup(row_width=1)
        error_markup.add(t.InlineKeyboardButton(text='🔨 Выгрузить логи', callback_data='unload_error_logs'))

        self.bot.send_message(chat_id, message, reply_markup = error_markup, parse_mode='Markdown')
    
    def admin_markup(self):
        admin_markup = t.InlineKeyboardMarkup(row_width=1)

        admin_markup.add(t.InlineKeyboardButton("Обновить ссылку на расписание", callback_data="update_parse_link"))
        admin_markup.add(t.InlineKeyboardButton("Обновить слоты (JSON)", callback_data="update_slots_json"))
        admin_markup.add(t.InlineKeyboardButton(text='🔨 Выгрузить логи', callback_data='unload_error_logs'))
        
        return admin_markup
    
    def missions_keyboard(self, active_idx: int) -> t.InlineKeyboardMarkup:
        labels = ["I", "II", "III", "IV"]
        buttons = [t.InlineKeyboardButton(text=lab, callback_data=f"mission:{i}") for i, lab in enumerate(labels)]
        keyboard = t.InlineKeyboardMarkup()
        keyboard.row(*buttons)
        keyboard.add(t.InlineKeyboardButton(text="Посмотреть на сайте", url=SOLID_GAMES_URL))
        return keyboard