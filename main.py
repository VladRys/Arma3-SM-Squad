from multiprocessing import Process
from telegram import telegram_init as telegram
from discord.discord_init import MainDiscord


# Run
if __name__ == "__main__":
    discord = Process(target=MainDiscord)
    discord.start()
    telegram = telegram.MainTelegram()

    discord.join()