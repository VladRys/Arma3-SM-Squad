from core.config import DB_FILE_PATH
from logs.setup_logs import setup_logger
from database.db import Database
from telegram import *

class Utils():
    def __init__(self):
        self.l = setup_logger()

    # === Loading All Telegram Extensions ===
    def load_ext(self, bot):
        try:
            db = Database(DB_FILE_PATH)
            commands = SlashCommands(bot)
            handlers = Handlers(bot, db)
            admin = AdminPanel(bot)
        except Exception as e:
            self.l.error(f"[LOAD EXTENSIONS ERROR] :{e}")
    
    