import telebot
from telebot import types as t
from telegram.commands.admin import AdminPanel
from telegram.utils.keyboards import CustomInlineKeyboards

from parser.parser import SolidGamesParser

from logs.setup_logs import unload_logs, unload_error_logs, setup_logger
from telegram.utils.utils import Formatter

class SlashCommands:
    def __init__(self, bot: telebot.TeleBot, parser: SolidGamesParser):
        self.bot = bot
        self.admin_panel = AdminPanel(self.bot)

        self.parser = parser

        self.custom_markups = CustomInlineKeyboards(self.bot)
        self.l = setup_logger()
        
        commands = [
            t.BotCommand("start", "Начать работу с ботом"),
            t.BotCommand("help", "Доступные команды"),
            t.BotCommand("missions", "Актуальные миссии"),
            t.BotCommand("admin", "Админ панель"),
            t.BotCommand("logs", "Просмотреть логи"),
        ]

        self.bot.set_my_commands(commands)

        self._register_commands(self.bot)

    def _register_commands(self, bot: telebot.TeleBot):
       
        @bot.message_handler(commands=["admin"])
        def handle_admin(self, message):
            self.admin_panel.admin_menu(message)

        @bot.message_handler(commands=["start"])
        def start(message):
            photo = open('telegram/src/patch_mc.jpg', 'rb')

            bot.send_photo(
                message.chat.id, photo, 
                caption=f"Вас приветствует виртуальный отряд СМЕРШ.\n\nВиртуальный отряд спец.назначения СМЕРШ был создан летом 2020-го года в качестве клана на базе игры H&G, где и базировался до марта 2023-го года. Закрытие Героев вынудили на тот момент еще клан искать новую площадку для своей игры. Этой игрой стала ARMA 3. За последние полтора года игры в неё клан посетил несколько крупных TVT и TVE проектов. В данный момент мы принимаем непосредственное участие в играх на проекте Red Bear, в его TVT1 и TVT2 режимах.\n\nДвигаемся в направлении более серьезной тактической игры и имеем дружное сообщество, которое радо и открыто к новичкам. Ведем открытый набор в наши ряды.\n\nРесурсы нашего отряда: \nЮтуб канал (☠️) - https://www.youtube.com/@SMERSH_HG\nДискорд - https://discord.gg/hXUSEWWxwW\nТимспик - SMERSH.TS3.RE\nТакже мы имеем закрытый телеграмм чат, доступ в который можно получить после одобрения заявки на вступление.",
            )
        @bot.message_handler(commands=["help"])
        def help(message):
            bot.send_message(message.chat.id, 
    """
    /missions - Отображение предстоящих миссий на основе расписания TVT
    /slots - Отображение наших слотов на предстоящих миссиях
    """)

        @bot.message_handler(commands=["missions"])
        def missions(message):
            latest = self.parser.parse_latest()
            if not latest:
                bot.send_message(message.chat.id, "Анонс не найден.")
                return

            missions = latest.get("missions", [])
            if not missions:
                bot.send_message(message.chat.id, "В анонсе нет миссий.")
                return

            text = Formatter.format_mission(missions, 0, latest.get("title"))
            keyboard = self.custom_markups.missions_keyboard(0)
            bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=keyboard)

        @bot.message_handler(commands=["logs"])
        def logs(message):
            unload_logs(bot, message)
            unload_error_logs(bot, message)
            

