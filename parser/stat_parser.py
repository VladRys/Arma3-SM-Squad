from bs4 import BeautifulSoup


class StatMissionsParser:
    def __init__(self):
        pass

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

        print(result)
        return result

    def format_stat_row(self, data: list) -> str:
        formatted_text = ""
        for item in data:
            name, score, faction = item
            if faction == "GUER": faction = "🟩"
            elif faction == "WEST": faction = "🟦"
            elif faction == "EAST": faction = "🟥"
            formatted_text += f"{faction} | {name} - {score}\n"
        return formatted_text

class StatParser:
    def __init__(self, missions_stats: StatMissionsParser):
        self.missions_stats = missions_stats