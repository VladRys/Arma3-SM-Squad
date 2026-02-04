from core.config import DB_FILE_PATH
from logs.setup_logs import setup_logger
from telegram import *

class Utils():
    def __init__(self):
        self.l = setup_logger()

    # === Loading All Telegram Extensions ===
    def load_ext(self, bot):
        try:
            commands = SlashCommands(bot)
            handlers = Handlers(bot, db)
            admin = AdminPanel(bot)
        except Exception as e:
            self.l.error(f"[LOAD EXTENSIONS ERROR] :{e}")
        