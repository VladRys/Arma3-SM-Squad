import disnake
from disnake.ext import commands
from logs.setup_logs import setup_logger    
from core.config import *

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.l=setup_logger()
        
        self.l.info("[DISCORD] Commands cog loaded successfully.")

def setup(bot):
    bot.add_cog(Commands(bot))
    