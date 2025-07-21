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
        top_mission_markup.add(t.InlineKeyboardButton(text='📈 Статистика отряда', callback_data=f'top_mission_squadstat'))
        
        return top_mission_markup

    def hide_squad_markup(self, msg):
        hide_squad_markup = t.InlineKeyboardMarkup(row_width=1)
        hide_squad_markup.add(t.InlineKeyboardButton(text='❌ Скрыть стату отряда', callback_data=f'hide_squad_stat_{msg}'))
        
        return hide_squad_markup
    
    def admin_markup(self):
        admin_markup = t.InlineKeyboardMarkup(row_width=1)

        admin_markup.add(t.InlineKeyboardButton("Обновить ссылку на расписание", callback_data="update_parse_link"))
        admin_markup.add(t.InlineKeyboardButton("Обновить слоты (JSON)", callback_data="update_slots_json"))
        admin_markup.add(t.InlineKeyboardButton(text='🔨 Выгрузить логи', callback_data='unload_error_logs'))
        
        return admin_markup