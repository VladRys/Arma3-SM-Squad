import sqlite3
import json

class Database:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        print("[+] Database")

    def close(self):
        self.conn.close()

    def get_slots(self):
        try:
            with open ("database/slots.json", "r", encoding="utf-8") as file: 
                slots = json.load(file)
                return slots
        except Exception as e:
            print('[JSON ERROR]', e)
