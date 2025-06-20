import subprocess
from telegram import telegram_init as telegram
from discord import discord_init as discord


# Run
if __name__ == "__main__":
    discord = subprocess.Popen(["python", "discord/discord_init.py"])
    telegram = telegram.MainTelegram()

    discord.wait()