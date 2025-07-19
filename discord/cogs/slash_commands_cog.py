import disnake

from disnake.ext import commands
from telegram.core.config import IMAGES_FOR_EMBED, EVERYONE_ROLE_ID
from parser.old_parser import anounce_pars, date
from main import BotDB as db
from parser.old_parser import parse

import random



class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Сообщение после запуска бота
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Commands Cog Ready!")
        
    @commands.has_role(1010609592608235560)
    @commands.slash_command(description="Обновить ссылку на анонс твт.")
    async def link(self, inter: disnake.ApplicationCommandInteraction, link: str):
        bot_channel = self.bot.get_channel(1265343421862907916)
        db.insert_link(link)
        print(link)
        await bot_channel.send("Ссылка была обновлена!")
    
    @commands.slash_command(description="Показывает список доступных слэш-команд")
    async def help(self, inter):
        bot_channel = self.bot.get_channel(1265343421862907916)
        embed = disnake.Embed(
            title="Доступные Команды",
            description="Список доступных команд бота",
        )
        embed.add_field(
            name="/announce",
            value="Команда для создания анонса на основе расписания твт игр. **Только для модераторов**",
            inline=False,
        )
        await bot_channel.send(embed=embed)
    
    
    
    @commands.slash_command(
        description="Команда для создания анонса на основе расписания твт игр"
    )
    @commands.has_role(1010609592608235560)
    async def anounce(self, inter):
        parse()
        random_number = random.randint(1, len(IMAGES_FOR_EMBED))
    
        bot_channel = self.bot.get_channel(1265343421862907916)
        ann_channel = self.bot.get_channel(1008819635879166052)
    
        role_mention = f"<@&{EVERYONE_ROLE_ID}>"
    
        embed = disnake.Embed(
            title="Анонс TVT2",  # Заголовок Embed
            description="Рад приветствовать бойцов СМЕРШ-а с новым анонсом!\n**ОТМЕЧАЕМСЯ КТО БУДЕТ!**",  # Описание Embed
            # color=disnake.Color.blue(),  # Цвет полоски слева
        )
        embed.set_author(
            name="Read Bear TvT", icon_url="https://www.red-bear.ru/img/gif.gif"
        )
        embed.add_field(
            name=f"{date[28].text}", value=f"\n{anounce_pars[2].text}", inline=False
        )
        embed.add_field(
            name=f"{date[39].text}",
            value=f"\n{anounce_pars[3].text}\n[Таблица Бронирования](https://docs.google.com/spreadsheets/d/1o68QMlEMg6TFV-59MjOBEOMkOGdKZM_gxrCOL9JRUKM/edit?usp=sharing)",
            inline=True,
        )
        embed.set_image(url=IMAGES_FOR_EMBED[random_number])
    
        await ann_channel.send(f"{role_mention}")
        await ann_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(SlashCommands(bot))