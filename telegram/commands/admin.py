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
            self.bot.send_message(message.chat.id, "Ты не являешься админом.")
            return False

    def admin_menu(self,message):
        user_id = message.from_user.id
        if self.is_admin(user_id, message):
            self.bot.send_message(message.chat.id, "Админ панель", reply_markup = self.custom_markups.admin_markup())