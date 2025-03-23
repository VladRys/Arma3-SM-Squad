import requests
import re
from bs4 import BeautifulSoup as BS



def fetch_html(url):
    """Запрашивает HTML-страницу и возвращает её содержимое."""
    response = requests.get(url)
    return BS(response.content, "html.parser")

def parse_missions():
    with open("parser/link.txt", "r") as file:
        link = file.read().strip()
    """Парсит миссии TVT и даты."""
    html = fetch_html(link)
    
    tables = html.find_all("table")
    dates = html.find_all("strong")
    
    mission_links = [a_tag["href"] for table in tables for a_tag in table.find_all("a", href=True)]
    
    tvt_titles = [dates[0].text, dates[27].text]  # Заголовки TVT 1 и TVT 2
    tvt_dates = [dates[1].text, dates[12].text, dates[27].text, dates[38].text]  # Даты для ТВТ
    
    tvt1_missions = clean_text([tables[0].text, tables[1].text])
    tvt2_missions = clean_text([tables[2].text, tables[3].text])
    
    return {
        "TVT_TITLES": tvt_titles,
        # "TVT_DATES": tvt_dates,
        "TVT1_MISSIONS": tvt1_missions,
        "TVT2_MISSIONS": tvt2_missions,
        "MISSION_LINKS": mission_links
    }

def clean_text(text_list):
    """Очищает текст от лишних пустых строк и пробелов."""
    return [re.sub(r"\n\s*\n+", "\n", text.strip()) for text in text_list]