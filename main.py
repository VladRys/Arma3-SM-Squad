from multiprocessing import Process
from telegram.telegram_init import MainTelegram
from discord.discord_init import MainDiscord

# Run
if __name__ == "__main__":
    # discord = Process(target=MainDiscord)
    # discord.start()
        
    telegram = Process(target=MainTelegram)
    telegram.start()

    # discord.join()
    telegram.join()