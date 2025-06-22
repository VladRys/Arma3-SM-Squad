import json
from pathlib import Path
from collections import UserDict

from core.config import TVT_DATES
class JSONStorage(UserDict):
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        super().__init__(data)

    def load_data(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

class SlotStorage(JSONStorage):
    def __init__(self):
        super().__init__("database/slots.json")
    
    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print('[JSON ERROR]', e)

    # === Simpler slots text format ===
    def get_slots_text(self):
        
        slots = self.load_data()

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
    
