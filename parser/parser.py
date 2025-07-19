import requests
import re
from bs4 import BeautifulSoup as BS

from parser.stat_parser import StatParser, StatMissionsParser, StatFormatter, MissionDownloader

from logs.setup_logs import setup_logger


class SiteParser():
    def __init__(self):
        self.logs = setup_logger()


    def fetch_html(self, url):
        response = requests.get(url)
        return BS(response.content, "html.parser")

    def parse_missions(self):
        with open("parser/link.txt", "r") as file:
            link = file.read().strip()
        
        html = self.fetch_html(link)

        tables = html.find_all("table")
        dates = html.find_all("strong")

        mission_links = [a_tag["href"] for table in tables for a_tag in table.find_all("a", href=True)]

        tvt_titles = [dates[0].text, dates[27].text]  # TVT Titles
        tvt_dates = [dates[1].text, dates[12].text, dates[27].text, dates[38].text]  # TVT Dates

        tvt1_missions = self.clean_text([tables[0].text, tables[1].text])
        tvt2_missions = self.clean_text([tables[2].text, tables[3].text])

        return {
            "TVT_TITLES": tvt_titles,
            # "TVT_DATES": tvt_dates,
            "TVT1_MISSIONS": tvt1_missions,
            "TVT2_MISSIONS": tvt2_missions,
            "MISSION_LINKS": mission_links
        }

    def clean_text(self, text_list):
        return [re.sub(r"\n\s*\n+", "\n", text.strip()) for text in text_list]

class Parser(SiteParser, StatParser):
    def __init__(self, missions_list: SiteParser, stats: StatParser, missions_stats: StatMissionsParser, stat_formatter: StatFormatter, mission_downloader: MissionDownloader):
        self.stats = stats(missions_stats, stat_formatter)
        super().__init__()