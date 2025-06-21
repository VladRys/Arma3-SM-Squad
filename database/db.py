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

    def get_slots(self):
        try:
            with open ("database/slots.json", "r", encoding="utf-8") as file: 
                slots = json.load(file)
                return slots
        except Exception as e:
            print('[JSON ERROR]', e)
    def get_slots_text(self):
        slots = self.get_slots()

        message_text = " "
        mode = 1
        day = 1
        game = 1 
        for i, d in enumerate(TVT_DATES):
            if i == 1:
                m = mode + 1
                d_ = day
            elif i == 3:
                m = mode + 1
                d_ = day + 1
            elif i == 2:
                m = mode
                d_ = day + 1
            else:
                m = mode
                d_ = day

            g1 = slots[f"TVT {m}"][f"Day {d_}"][f"Game {game}"]
            g2 = slots[f"TVT {m}"][f"Day {d_}"][f"Game {game+1}"]
            message_text += f"{d}\n1 ИГРА: {g1}\n2 ИГРА: {g2}\n\n"

        return message_text