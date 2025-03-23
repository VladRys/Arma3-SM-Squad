import requests
import sqlite3
import re
from bs4 import BeautifulSoup as BS
from main import BotDB as db


with open ("parser/link.txt", "r") as file:
    link = file.read()


r = requests.get(link)
html = BS(r.content, "html.parser")

# Получаем все теги тейбл на сайте
anounce_pars = html.find_all("table")
date = html.find_all("strong")
mission_links = []

for table in anounce_pars:
    for a_tag in table.find_all("a", href=True):  # Ищем теги <a> с атрибутом href
        mission_links.append(a_tag["href"])
        
TVT1_MISSIONS = []
TVT2_MISSIONS = []

TVT = [date[0].text, date[26].text] # TVT 1, TVT 2

def parse():

    r = requests.get(link)
    html = BS(r.content, "html.parser")
    
    # Получаем все теги тейбл на сайте
    anounce_pars = html.find_all("table")
    date = html.find_all("strong")
    

    # # Миссии ТВТ 1
    # print(date[0].text) # TVT 1

    # print(date[1].text) # Дата четверга
    # print(anounce_pars[0].text)
    # print(date[12].text) # Дата Субботы
    # print(anounce_pars[1].text)
    
    # # Вывод тегов тейбл для твт 2 Миссии ТВТ 2
    # print(date[26].text) # TVT 2
    # print(date[27].text)  # Дата пятницы
    # print(anounce_pars[2].text)
    # print(date[38].text)  # Дата субботы
    # print(anounce_pars[3].text)
    # # Вывод тегов стронг для твт2
    # print(mission_links)
    
parse()

def clearing_text(array):
    if array == TVT1_MISSIONS:
        i = 0
        while i <= 1:
            clean_text = re.sub(r"\n\s*\n+", "\n", anounce_pars[i].text)
            array.append(clean_text)
            print(clean_text)
            i+=1
    else:
        i=2
        while i <= 3:
            clean_text = re.sub(r"\n\s*\n+", "\n", anounce_pars[i].text)
            array.append(clean_text)
            print(clean_text)
            i+=1
 
clearing_text(TVT1_MISSIONS)
clearing_text(TVT2_MISSIONS)

DATES = [date[1].text, date[12].text, date[27].text, date[38].text]


print(TVT1_MISSIONS)
print(TVT2_MISSIONS)