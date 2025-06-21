from disnake.ext import commands
from logs.setup_logs import setup_logger

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.l = setup_logger()
        self.l.info("[DISCORD] EventHandler cog loaded successfully.")

    async def on_ready(self):
        await self.bot.sync_commands()
        self.l.info("[DISCORD] Commands synced successfully.")

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
def setup(bot):
    bot.add_cog(EventHandler(bot))