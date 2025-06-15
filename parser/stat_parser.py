import requests

url = "https://stats.red-bear.ru/total_tvt"
headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(url, headers=headers)
html = resp.text

print(html)