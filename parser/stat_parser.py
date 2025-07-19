import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

import re

from logs.setup_logs import setup_logger

from core.config import STAT_SITE_URL

class MissionDownloader:
    def __init__(self):
        self.logs = setup_logger()
        
    def get_ocap_missions(self) -> list:
        response = requests.get(STAT_SITE_URL)
        html =  BeautifulSoup(response.content, "html.parser")

        tables = html.find_all("tbody")
        mission_links = ["https://stats.red-bear.ru/" + a_tag["href"] for table in tables for a_tag in table.find_all(class_ = "replay_id")]
        
        print(mission_links[-10:0])
        
        return mission_links
    
    def update_missions(self):
        links = self.get_ocap_missions()
        # for link in links:
        #     self.download_mission(link)
    
    def download_mission(self, url: str):
        response = requests.get(url)

        if response.status_code == 200:
            mission_name = StatFormatter.get_mission_name_by_url(url)

            with open(f"parser/ocap_missions/{mission_name}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
                self.logs.info(f"[PARSER] Миссия {mission_name} успешно загружена!")
                
        else:
            print("Ошибка:", response.status_code)
            self.logs.error("[PARSER] Ошибка при загрузке миссии")

class StatMissionsParser:
    def __init__(self, mission_downloader: MissionDownloader):
        self.mission_downloader = mission_downloader()

    def parse_top_mission_stat(self, mission_name, squads: bool = False, players: bool = False) -> list:
        with open(f"parser/ocap_missions/{mission_name}.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        rows = soup.find_all("tr", class_=["odd", "even"])

        result = []
        for row in rows[10::]:
            try: 
                cells = row.find_all("td")
                name = cells[0].get_text(strip=True)
                score = cells[1].get_text(strip=True)
                faction = cells[2].get_text(strip=True)
                
                if players and name.startswith("["):
                    result.append((name, score, faction))
                elif squads and not name.startswith("["):
                    result.append((name, score, faction))

            except IndexError:
                break

        return result

class StatFormatter():
    def side_formatter(self, text):
        if text == "GUER": faction = "🟩"
        elif text == "WEST": faction = "🟦"
        elif text == "EAST": faction = "🟥"
        
        return faction
    
    def format_stat_row(self, data: list) -> str:
        formatted_text = ""
        for item in data:
            name, score, faction = item
            faction = self.side_formatter(faction)
           
            formatted_text += f"{faction} | {name} - {score}\n"
        return formatted_text
    
    
    def get_mission_name_by_url(url: str) -> str:
        params = parse_qs(urlparse(url).query)
        filename = params.get("filename")
        if not filename:
            return None

        filename = filename[0]  

        part = filename.split("__")[-1]  

        if part[2] == "_" and part[5] == "_":
            part = part[6:]  

        mission_name = part.replace(".json", "")
        return mission_name

class StatParser:
    def __init__(self, missions_stats: StatMissionsParser, stat_formatter: StatFormatter):
        self.missions_stats = missions_stats(MissionDownloader)
        self.stat_formatter = stat_formatter()
        