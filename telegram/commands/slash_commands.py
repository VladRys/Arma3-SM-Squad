
from telebot import types as t
from database.db import Database
from database.slots import SlotStorage

from core.config import  ADMINS, DB_FILE_PATH, TVT_DATES
from core.exceptions import MissionIndexException
from telegram.commands.admin import AdminPanel
from telegram.utils.keyboards import CustomInlineKeyboards
from telegram.utils.donate import Donate

from parser.parser import Parser, SiteParser, StatParser, StatMissionsParser, StatFormatter

from logs.setup_logs import unload_logs, unload_error_logs, setup_logger

class SlashCommands():
    def __init__(self, bot):
        self.bot = bot
        self.db = Database(DB_FILE_PATH)
        
        self.admin_panel = AdminPanel(self.bot)

        self.parser = Parser(SiteParser, StatParser, StatMissionsParser, StatFormatter)
        
        self.slots = SlotStorage()
        
        self.donate = Donate(self.bot)

        self.custom_markups = CustomInlineKeyboards(self.bot)
        self.l = setup_logger()
        
        commands = [
            t.BotCommand("start", "Начать работу с ботом"),
            t.BotCommand("help", "Доступные команды"),
            t.BotCommand("missions", "Актуальные миссии"),
            t.BotCommand("slots", "Актулальные слоты"),
            t.BotCommand("admin", "Админ панель"),
            t.BotCommand("donate", "Кинуть копейку на хост"),
            t.BotCommand("mission_stat", "Топ игроков и отрядов на последней миссии"),
            t.BotCommand("logs", "Просмотреть логи"),
        ]

        self.bot.set_my_commands(commands)

        self.bot.message_handler(commands=["start"])(self.start)
        self.bot.message_handler(commands=["missions"])(self.missions)
        self.bot.message_handler(commands=["slots"])(self.show_slots)
        self.bot.message_handler(commands=["admin"])(self.handle_admin)
        self.bot.message_handler(commands=["mission_stat"])(self.top_mission_stat)
        self.bot.message_handler(commands=["donate"])(self.donate_pls)

        self.bot.message_handler(commands=["help"])(self.help)

        self.bot.message_handler(commands=["logs"])(self.logs)
    
    def handle_admin(self, message):
        self.admin_panel.admin_menu(message)

    def start(self, message):
        photo = open('telegram/src/patch_mc.jpg', 'rb')

        self.bot.send_photo(
            message.chat.id, photo, 
            caption=f"Вас приветствует виртуальный отряд СМЕРШ.\n\nВиртуальный отряд спец.назначения СМЕРШ был создан летом 2020-го года в качестве клана на базе игры H&G, где и базировался до марта 2023-го года. Закрытие Героев вынудили на тот момент еще клан искать новую площадку для своей игры. Этой игрой стала ARMA 3. За последние полтора года игры в неё клан посетил несколько крупных TVT и TVE проектов. В данный момент мы принимаем непосредственное участие в играх на проекте Red Bear, в его TVT1 и TVT2 режимах.\n\nДвигаемся в направлении более серьезной тактической игры и имеем дружное сообщество, которое радо и открыто к новичкам. Ведем открытый набор в наши ряды.\n\nРесурсы нашего отряда: \nЮтуб канал (☠️) - https://www.youtube.com/@SMERSH_HG\nДискорд - https://discord.gg/hXUSEWWxwW\nТимспик - SMERSH.TS3.RE\nТакже мы имеем закрытый телеграмм чат, доступ в который можно получить после одобрения заявки на вступление.",
        )

    def donate_pls(self, message):
        self.donate.send_invoice_message(message)
        
    def help(self, message):
        self.bot.send_message(message.chat.id, 
"""
/missions - Отображение предстоящих миссий на основе расписания TVT
/slots - Отображение наших слотов на предстоящих миссиях
/mission_stat - Стата топ игроков по последней миссии. Команда поддерживает индекс миссии -1 -2 -3, (позапрошлая, позапозапоршлая и т.д.) до -9
/missions_stat -1 - Топ стата на позапрошлой миссии
/donate - Закинуть копейку на хост 
""")

    # === Top Mission Stat ===
    def top_mission_stat(self, message):
        if len(message.text.split()) > 1:
            try:
                mission_index = int(message.text.split()[1])
                if mission_index > 0 and mission_index < -10:
                    self.bot.send_message(message.chat.id, "Номер миссии должен быть меньше 0 и больше -10") 
                    raise MissionIndexException("Mission index must be less than 0", mission_index)
            except ValueError:
                raise MissionIndexException("Mission index must be an integer", 0)
        else:
            mission_index = 0
        
        try:
            msg = self.bot.send_message(message.chat.id, 'Получаю статистику..... (это может занять время)', parse_mode='Markdown')
            stat, mission_name, mission_link = self.parser.stats.missions_stats.parse_top_mission_stat(
            mission_index, squads=True, players=True
            )

            with open("parser/ocap_missions/active_mission.txt", "w", encoding="utf-8") as f:
                f.write(mission_link)

            formatted_stat = self.parser.stats.stat_formatter.format_stat_row(stat)
            rows = formatted_stat.strip().split("\n")

            for i in range(len(rows) - 1):
                try:
                    if i > 9:
                        rows.insert(i, "")
                        rows.insert(i, "Top Squads:") 
                        rows.insert(i, "")
                        break
                except IndexError:
                    continue

            formatted_stat = "\n".join(rows)


            self.bot.edit_message_text(
                f"Топ игроков и отрядов на миссии {mission_name}\n\nTop Players:\n\n{formatted_stat}", chat_id = message.chat.id, message_id = msg.message_id
            )
            self.bot.edit_message_reply_markup(chat_id = message.chat.id, message_id = msg.message_id, reply_markup = self.custom_markups.top_mission_markup())
        except Exception as e:
            self.custom_markups.get_error_markup(message.chat.id, 'Ошибка во время получения статистики по миссии')
            self.l.error(f"[ERROR] while handling mission stats {mission_name}: {e}")

    # === fixed dates ===
    def missions(self, message):
        parsed_data = self.parser.parse_missions()
        markup = t.InlineKeyboardMarkup()
        button = t.InlineKeyboardButton("Скачать Миссии", callback_data="download_missions")
        markup.add(button)

        text = f"*RED BEAR TVT 1*\n{TVT_DATES[0]}\n{parsed_data['MISSIONS'][0]}\n\n{TVT_DATES[1]}\n{parsed_data['MISSIONS'][1]}\n\n{TVT_DATES[2]}\n{parsed_data['MISSIONS'][2]}"

        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    
    def show_slots(self, message):
        self.bot.send_message(message.chat.id, self.slots.get_slots_text())

    def logs(self, message):
        unload_logs(self.bot, message)
        unload_error_logs(self.bot, message)
        
