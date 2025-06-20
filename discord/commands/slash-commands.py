import disnake
from disnake.ext import commands
from logs.setup_logs import setup_logger    


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.l=setup_logger()
        self.bot_channel = self.bot.get_channel(1265343421862907916)
    
    @commands.slash_command(description="Отправляет сообщение от имени бота")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        embed_my = disnake.Embed(
            title="Команды",
            description="""
            Доступные команды:
            Еще что-то..
            """
            
        )
        await self.bot_channel.send(embed = embed_my)
    
    
def setup(bot):
    bot.add_cog(Commands(bot))
    