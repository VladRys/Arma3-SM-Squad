from logs.setup_logs import setup_logger
from telegram import SlashCommands, Handlers, AdminPanel
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from parser.parser import SolidGamesParser

class Utils():
    def __init__(self):
        self.l = setup_logger()

    # === Loading All Telegram Extensions ===
    def load_ext(self, bot):
        try:
            
            options = Options()
            options.add_argument("--lang=ru-RU")
            options.add_argument("--start-maximized")
            options.add_experimental_option(
                "prefs", {"intl.accept_languages": "ru,ru-RU"}
            )

            driver = Chrome(options=options)

            parser = SolidGamesParser(driver)
            parser.load_page()
            commands = SlashCommands(bot, parser)
            handlers = Handlers(bot, parser)
            admin = AdminPanel(bot)
            
        except Exception as e:
            self.l.error(f"[LOAD EXTENSIONS ERROR] :{e}")