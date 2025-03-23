import subprocess
from database.db import BotDB
from core.config import DB_FILE_PATH

# Database setup
BotDB = BotDB(DB_FILE_PATH)

# Run
if __name__ == "__main__":
    # process1 = subprocess.Popen(["python", "ds_bot.py"])
    process2 = subprocess.Popen(["python", "telegram_bot.py"])
    
    # process1.wait()
    process2.wait()