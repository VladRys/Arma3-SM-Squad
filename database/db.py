import sqlite3
import json

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            """
       CREATE TABLE IF NOT EXISTS link_for_parser (
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
           link TEXT NOT NULL
       );
       """
        )

        self.cursor.execute(
            """
       CREATE TABLE IF NOT EXISTS Slots (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           day_1 TEXT NOT NULL,
           day_1_first_game_slots TEXT,
           day_1_first_game_color TEXT,
           day_1_second_game_slots TEXT,
           day_1_second_game_colors TEXT,
           day_2 TEXT NOT NULL,
           day_2_first_game_slots TEXT,
           day_2_first_game_color TEXT,
           day_2_second_game_slots TEXT,
           day_2_second_game_colors TEXT
       );
       """
        )
        self.conn.commit()


        print("[+] Database")


    def insert_link(self, anounce_link):
        update_query = "UPDATE link_for_parser SET link = ?"
        self.cursor.execute("UPDATE link_for_parser SET link = (?)", (anounce_link,))
        return self.conn.commit()

    def close(self):
        self.conn.close()

    def get_slots(self):
        try:
            with open ("database/slots.json", "r", encoding="utf-8") as file: 
                slots = json.load(file)
                return slots
        except Exception as e:
            print('[JSON ERROR]', e)


    def update_slots(self, mode, day, game, value):
        data = self.get_slots()
        data[mode][day][game] = value
        try:
            with open ("database/slots.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                print(data)
        except Exception as e:
            print('[JSON ERROR]', e)