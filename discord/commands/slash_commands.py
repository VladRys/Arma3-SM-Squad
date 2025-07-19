import disnake
from disnake.ext import commands
from logs.setup_logs import setup_logger    
from core.config import *

from database.db import Database
from database.slots import SlotStorage

from parser.parser import Parser, SiteParser, StatParser, StatMissionsParser, StatFormatter, MissionDownloader

import random

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.l=setup_logger()
        self.parser = Parser(SiteParser, StatParser, StatMissionsParser, StatFormatter, MissionDownloader)
        self.db = Database(DB_FILE_PATH)
        self.slots = SlotStorage()
        
        self.l.info("[DISCORD] Commands cog loaded successfully.")


    @commands.slash_command(name="помощь", description="Показать список доступных команд")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        bot_channel = self.bot.get_channel(BOT_CHANNEL_ID)
        
        desc = ""

        for cmd in self.bot.slash_commands:
            desc += f"**/{cmd.name}** - {cmd.description or "Без описания"}\n"    
        
        embed = disnake.Embed(
            title="Доступные Команды",
            description=desc,
            color=EMBED_COLOR
        )
        await bot_channel.send(embed = embed)
    
    @commands.has_role(MODERATOR_ROLE_ID)
    @commands.slash_command(name="анонс", description="Создать анонс на основе расписания TVT игр")
    async def anounce(self, inter: disnake.ApplicationCommandInteraction):
        bot_channel = self.bot.get_channel(BOT_CHANNEL_ID)
        ann_channel = self.bot.get_channel(ANN_CHANNEL_ID)
        
        role_mention = f"<@&{EVERYONE_ROLE_ID}>"
        
        parsed_data = self.parser.parse_missions()

        mission_embed = disnake.Embed(
            title="Миссии TVT",
            description=f"Ближайшие миссии на эту неделю:",
            color=EMBED_COLOR
        )

        mission_embed.set_author(
            name="Read Bear TvT", icon_url="https://www.red-bear.ru/img/gif.gif"
        )

        mission_embed.add_field(
            name="TVT I",
            value=f"**{TVT_DATES[0]}**\n{parsed_data['TVT1_MISSIONS'][0]}\n\n**{TVT_DATES[2]}**\n{parsed_data['TVT1_MISSIONS'][1]}",
        )
        mission_embed.add_field(
            name="TVT II",
            value=f"**{TVT_DATES[1]}**\n{parsed_data['TVT2_MISSIONS'][0]}\n\n**{TVT_DATES[3]}**\n{parsed_data['TVT2_MISSIONS'][1]}",
        )
        slots_embed = disnake.Embed(
            title="Слоты на TVT",
            description=f"Список слотов на ближайшие TVT игры:\n\n{self.slots.get_slots_text()}",
            color=EMBED_COLOR
        )
        slots_embed.set_author(
            name="Read Bear TvT", icon_url="https://www.red-bear.ru/img/gif.gif"
        )
        slots_embed.set_image(url=IMAGES_FOR_EMBED[random.randint(0, len(IMAGES_FOR_EMBED) - 1)])
        
        if TEST_MODE:
            await bot_channel.send("Анонс успешно отправлен!")
            await bot_channel.send("Анонс", embed=mission_embed)
            await bot_channel.send("", embed=slots_embed)

        else:
            await bot_channel.send("Анонс успешно отправлен!")
            await ann_channel.send(role_mention, embed=mission_embed)
            await ann_channel.send("", embed=slots_embed)

def setup(bot):
    bot.add_cog(Commands(bot))
    