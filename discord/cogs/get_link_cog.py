import disnake
from disnake.ext import commands
import re

class GetLink(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.target_word = "РАСПИСАНИЕ ИГР ТVТ"


    def find_url(self, message):
        url_pattern = r"(https?://[^\s]+)"
        match = re.search(url_pattern, message)
        return match.group(0) if match else None
        
    # Обработчик событий для сообщений
    @commands.Cog.listener()
    async def on_message(self, message):
    
        # Проверяем, что сообщение не от бота
        if message.author == self.bot.user:
            return
    
        # Проверка на наличие ссылки
    
        url = self.find_url(message.content)
    
        # Проверка на наличие определенного слова
        if url and self.target_word in message.content:
            # Записываем ссылку в переменную
            print(f"Найдена ссылка: {url} в сообщении: {message.content}")
            with open("link.txt", "w") as file:
                file.write(url)
        # Не забываем обрабатывать другие команды бота
        await self.bot.process_commands(message)
        
def setup(bot):
    bot.add_cog(GetLink(bot))