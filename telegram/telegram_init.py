import telebot 

import time

from core import config, utils 
from logs.setup_logs import setup_logger

class MainTelegram():
    def __init__(self):
        self.bot = telebot.TeleBot(config.MAIN_TOKEN_TELEGRAM)

        self.logs = setup_logger()
        self.utils = utils.Utils()
    
        self.main()
    
    def main(self):
        try:
            self.utils.load_ext(self.bot)    
            print("[+++] Telegram")
            self.logs.info(f"Bot online in {config.MODE} mode")
            while True:
                try:
                    self.bot.polling(config.MAIN_TOKEN_TELEGRAM)
                except telebot.apihelper.ApiHTTPException as e:
                    print("[TELEGRAM] ApiHTTPException Error: Restarting")
                    time.sleep(5)
                except telebot.apihelper.ConnectionError as e:
                    print("[ERROR]", e)
                    self.logs.error(f"[TELEGRAM] Connection Error: Restarting")
                    time.sleep(5)   

                except Exception as e:
                    print("[ERROR]", e)
                    self.logs.error(f"[ERROR] while bot online: {e}")
 
        except Exception as e:
            print("[ERROR]", e)
            self.logs.error(f"[ERROR] while start bot: {e}")
            