import disnake
from disnake.ext import commands
from core import config

class MainDiscord:
    def __init__(self):

        self.intents = disnake.Intents.all()
        self.command_sync_flags = commands.CommandSyncFlags.default()
        self.command_sync_flags.sync_commands_debug = True
        
        self.bot = commands.Bot(
            command_prefix="/", intents=self.intents, command_sync_flags=self.command_sync_flags
        )
    
        self.main()

    def main(self):
        print("[+++] Discord")       
        initial_extensions = []

        for extension in initial_extensions:
            self.bot.load_extension(extension)

        self.bot.run(config.TOKEN_DISCORD)
