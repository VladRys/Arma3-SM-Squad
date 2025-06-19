import telebot 

from core import config, utils 
from logs.setup_logs import setup_logger

class MainTelegram():
    def __init__(self):
        self.config = config
        self.bot = telebot.TeleBot(self.config.MAIN_TOKEN_TELEGRAM)

        self.logs = setup_logger()
        self.utils = utils.Utils()
    
        self.main()
    
    def main(self):
        try:
            self.utils.load_ext(self.bot)    
            print("[+++] Telegram")
            self.logs.info(f"Bot online in {config.MODE} mode")
            self.bot.polling(config.MAIN_TOKEN_TELEGRAM)
            
        except Exception as e:
            print("[ERROR]", e)
            self.logs.error(f"[ERROR] while bot online: {e}")
            