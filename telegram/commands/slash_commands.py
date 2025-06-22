from telebot import types as t
from database.db import Database
from database.slots import SlotStorage

from core.config import  ADMINS, DB_FILE_PATH, TVT_DATES
from telegram.commands.admin import AdminPanel

from parser.parser import Parser

class SlashCommands():
    def __init__(self, bot):
        self.bot = bot
        self.db = Database(DB_FILE_PATH)
        
        self.admin_panel = AdminPanel(self.bot)

        self.parser = Parser()
        
        self.slots = SlotStorage()

        commands = [
            t.BotCommand("start", "Начать работу с ботом"),
            t.BotCommand("missions", "Актуальные миссии"),
            t.BotCommand("slots", "Актулальные слоты")
        ]

        self.bot.set_my_commands(commands)

        self.bot.message_handler(commands=["start"])(self.start)
        self.bot.message_handler(commands=["missions"])(self.missions)
        self.bot.message_handler(commands=["slots"])(self.show_slots)
        self.bot.message_handler(commands=["admin"])(self.handle_admin)
    
    def handle_admin(self, message):
        self.admin_panel.admin_menu(message)

    def start(self, message):
        photo = open('telegram/src/patch_mc.jpg', 'rb')

        self.bot.send_photo(
            message.chat.id, photo, 
            caption=f"Вас приветствует виртуальный отряд СМЕРШ.\n\nВиртуальный отряд спец.назначения СМЕРШ был создан летом 2020-го года в качестве клана на базе игры H&G, где и базировался до марта 2023-го года. Закрытие Героев вынудили на тот момент еще клан искать новую площадку для своей игры. Этой игрой стала ARMA 3. За последние полтора года игры в неё клан посетил несколько крупных TVT и TVE проектов. В данный момент мы принимаем непосредственное участие в играх на проекте Red Bear, в его TVT1 и TVT2 режимах.\n\nДвигаемся в направлении более серьезной тактической игры и имеем дружное сообщество, которое радо и открыто к новичкам. Ведем открытый набор в наши ряды.\n\nРесурсы нашего отряда: \nЮтуб канал (☠️) - https://www.youtube.com/@SMERSH_HG\nДискорд - https://discord.gg/hXUSEWWxwW\nТимспик - SMERSH.TS3.RE\nТакже мы имеем закрытый телеграмм чат, доступ в который можно получить после одобрения заявки на вступление.",
        )

    # === fixed dates ===
    def missions(self, message):
        parsed_data = self.parser.parse_missions()
        markup = t.InlineKeyboardMarkup()
        button = t.InlineKeyboardButton("Скачать Миссии", callback_data="download_missions")
        markup.add(button)

        tvt1 = f"*RED BEAR TVT 1*\n{TVT_DATES[0]}\n{parsed_data['TVT1_MISSIONS'][0]}\n\n{TVT_DATES[2]}\n{parsed_data['TVT1_MISSIONS'][1]}\n\n"
        tvt2 = f"*RED BEAR TVT 2*\n{TVT_DATES[1]}\n{parsed_data['TVT2_MISSIONS'][0]}\n\n{TVT_DATES[3]}\n{parsed_data['TVT2_MISSIONS'][1]}"

        text = tvt1 + tvt2

        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    
    def show_slots(self, message):
        slots = self.slots.load_data()

        message_text = " "
        mode = 1
        day = 1
        game = 1 
        for i, d in enumerate(TVT_DATES):
            if i == 1:
                m = mode + 1
                d_ = day
            elif i == 3:
                m = mode + 1
                d_ = day + 1
            elif i == 2:
                m = mode
                d_ = day + 1
            else:
                m = mode
                d_ = day

            g1 = slots[f"TVT {m}"][f"Day {d_}"][f"Game {game}"]
            g2 = slots[f"TVT {m}"][f"Day {d_}"][f"Game {game+1}"]
            message_text += f"{d}\n|\n1 ИГРА: {g1}\n2 ИГРА: {g2}\n|\n"

        self.bot.send_message(message.chat.id, message_text)