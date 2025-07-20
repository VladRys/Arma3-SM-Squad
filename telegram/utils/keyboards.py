from telebot import types as t

class CustomInlineKeyboards():
    def __init__(self, bot):
        self.bot = bot
        
    def get_error_markup(self, chat_id, message):
        error_markup = t.InlineKeyboardMarkup(row_width=1)
        error_markup.add(t.InlineKeyboardButton(text='🔨 Выгрузить логи', callback_data='unload_error_logs'))

        self.bot.send_message(chat_id, message, reply_markup = error_markup, parse_mode='Markdown')
    
    def top_mission_markup(self):
        top_mission_markup = t.InlineKeyboardMarkup(row_width=1)
        top_mission_markup.add(t.InlineKeyboardButton(text='📈 Статистика отряда', callback_data='top_mission_squad_stat'))
        
        return top_mission_markup
