import sqlite3
import json

from core.config import TVT_DATES

class Database:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        print("[+] Database")

    def close(self):
        self.conn.close()
