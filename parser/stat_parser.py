import requests
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from collections import defaultdict

from logs.setup_logs import setup_logger

from core.config import STAT_SITE_URL

class SeleniumDriver:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)

        self.logs = setup_logger()


    def close(self):
        self.driver.quit()

class MissionDownloader(SeleniumDriver):
    def __init__(self):
        super().__init__()

    def download_mission(self, url: str):
        headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)


        self.driver.get(url)

        filename = StatFormatter.get_mission_name_by_url(url)
        html = self.driver.page_source
        with open("parser/ocap_missions/mission.html", "w", encoding="utf-8") as f:
            f.write(html)
            self.logs.info(f"Mission downloaded and saved as {filename}")
            return filename


    def get_missions(self):
        response = requests.get(STAT_SITE_URL)
        html =  BeautifulSoup(response.content, "html.parser")

        tables = html.find_all("tbody")
        mission_links = [
            "https://stats.red-bear.ru/" + a_tag["href"]
            for table in tables
            for a_tag in table.find_all(class_="replay_id")
        ][-10:]

        print(mission_links)

        return mission_links

class StatMissionsParser:
    def __init__(self, mission_downloader: MissionDownloader):
        self.mission_downloader = mission_downloader
        self.driver = self.mission_downloader.driver

        self.logs = setup_logger()


    def smersh_top_mission_stat(self, url) -> list:
        self.driver.get(url)
        time.sleep(1)


        smersh_stats = set()

        while True:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            table = soup.find("table", {"id": "stats-table"})
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 5:
                        player = cols[0].get_text(strip=True)
                        frags = cols[1].get_text(strip=True)
                        tk = cols[4].get_text(strip=True)

                        if "[СМЕРШ]" in player:
                            frags = int(frags) if frags.isdigit() else 0
                            tk = int(tk) if tk.isdigit() else 0
                            smersh_stats.add((player, frags, tk))

            next_btn = self.driver.find_element(By.ID, "stats-table_next")
            if "disabled" in next_btn.get_attribute("class"):
                break
            self.driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(0.5)

        lines = []
        for name, frags, tk in sorted(smersh_stats, key=lambda x: -x[1]):
            if "[СМЕРШ]" in name:
                name = f"🪖 | {name.replace("[СМЕРШ]", "").strip()}"

            line = f"{name} - {frags} фрагов"
            if tk > 0:
                line += f", {tk} грех(а)"
            lines.append(line)

        print(lines)
        return "\n".join(lines)
    
    def parse_top_mission_stat(self, mission_index: int = 0, squads: bool = False, players: bool = False) -> list:
        
        missions_urls = self.mission_downloader.get_missions()
        url = missions_urls[-1 + mission_index]
        mission_name = self.mission_downloader.download_mission(url)

        with open(f"parser/ocap_missions/mission.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        rows = soup.find_all("tr", class_=["odd", "even"])

        result = []
        for row in rows[10::]:
            try: 
                cells = row.find_all("td")
                name = cells[0].get_text(strip=True)
                score = cells[1].get_text(strip=True)
                faction = cells[2].get_text(strip=True)
                
                result.append((name, score, faction))


            except IndexError:
                break
            
        if not result:
            self.logs.info("Mission was parsed not properly")
        else:
            self.logs.info("[+++] Mission was parsed properly!") 
        
            
        return result, mission_name, url

class StatFormatter:
    def side_formatter(self, text):
        if text == "GUER": text = "🟢"
        elif text == "WEST": text = "🔵"
        elif text == "EAST": text = "🔴"
        else:
            text = "❓"
        
        return text
    
    def format_stat_row(self, data: list) -> str:
        formatted_text = ""
        for item in data:
            name, score, faction = item
            faction = self.side_formatter(faction)
            if "no_side" in name:
                name = name.replace("no_side", "").strip()
            
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


    def escape_markdown(self, text):
        escape_chars = r'\_*[]()~`>#+-=|{}.!'
        return re.sub(rf'([{re.escape(escape_chars)}])', r'\\\1', text)

class StatParser:
    def __init__(self, missions_stats: StatMissionsParser, stat_formatter: StatFormatter):
        self.missions_stats = missions_stats(MissionDownloader())
        self.stat_formatter = stat_formatter()
