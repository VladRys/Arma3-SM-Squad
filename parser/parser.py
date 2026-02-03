import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from core.config import SOLID_GAMES_URL, ALLOWED_TITLES, FEED_ITEM_PARSE_LIMIT, SELECTORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolidGamesParser:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self):
        try:
            logger.info(f"Загружаем страницу: {SOLID_GAMES_URL}")
            self.driver.get(SOLID_GAMES_URL)
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_elements(By.CLASS_NAME, "feed-item")
            )
            logger.info("Page succesfully loaded.")
        except Exception as e:
            logger.exception(f"Error while load page: {e}")

    def parse_announcement(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            sections = []

            for feed in soup.select(SELECTORS["feed_item"])[:FEED_ITEM_PARSE_LIMIT]:
                try:
                    title_el = feed.select_one(SELECTORS["section_header_title"])
                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    if not any(title.startswith(t) for t in ALLOWED_TITLES):
                        continue

                    missions = self.parse_missions(feed)
                    sections.append({"title": title, "missions": missions})
                except Exception as e:
                    logger.exception(f"Error while parsing feed-item: {e}")

            return sections
        except Exception as e:
            logger.exception(f"Error while parsing page: {e}")
            return []

    def parse_latest(self):
        sections = self.parse_announcement()
        return sections[0] if sections else None

    def parse_missions(self, feed):
        missions = []

        try:
            tabs_container = feed.select_one(SELECTORS["tabs_container"])
            ann_content = feed.select_one(".feed-ann-content")  

            tabs = tabs_container.select(SELECTORS["tab_button"]) if tabs_container else feed.select(SELECTORS["tab_button"])
            blocks = ann_content.select(SELECTORS["mission_block"]) if ann_content else feed.select(SELECTORS["mission_block"])

            candidate_blocks = [
                b for b in blocks
                if b.select_one(SELECTORS["mission_desc_item"]) or b.select_one(SELECTORS["preview_spoiler"])
            ]

            for tab, block in zip(tabs, candidate_blocks):
                try:
                    name_el = tab.select_one(SELECTORS["desktop_tab_name"])
                    name = name_el.get_text(strip=True) if name_el else "Unknown"
                    info = self.parse_mission_block(block)
                    missions.append({"name": name, "info": info})
                except Exception as e:
                    logger.exception(f"Error while parsing mission: {e}")
        except Exception as e:
            logger.exception(f"Error while parse missions feed-item: {e}")

        return missions

    def parse_mission_block(self, block):
        result = {"map": None, "time": None, "servers": [], "description": None}
        current_server = None

        def extract_sides(el):
            sides = {}
            for tag in el.find_all(True):
                for cls in tag.get("class", []):
                    if cls.endswith("-side"):
                        sides[cls] = tag.get_text("\n", strip=True)
                        break
            return sides

        try:
            for wrapper in block.find_all(recursive=False):
                if wrapper.get("class") and "mobile-item" in wrapper.get("class"):
                    continue

                if wrapper.name == "div":
                    for el in wrapper.find_all(recursive=False):
                        try:
                            server = self._extract_server_label(el)
                            if server:
                                current_server = server
                                result["servers"].append(current_server)
                                continue
                            current_server = self._process_server_data(el, current_server, result)
                        except Exception as e:
                            logger.exception(f"Error while fetching mission block element: {e}")
        except Exception as e:
            logger.exception(f"Error while avoiding wrapper in mission block: {e}")

        try:
            spoiler = block.select_one(SELECTORS["preview_spoiler"])
            if spoiler:
                result["description"] = {
                    "text": spoiler.get_text("\n", strip=True),
                    "links": [a["href"] for a in spoiler.select("a[href]")]
                }
        except Exception as e:
            logger.exception(f"Error while parse mission description: {e}")

        flat_equipment = {}
        for srv in result.get("servers", []):
            flat_equipment.update(srv.get("equipment", {}))
            for k, v in srv.get("sides", {}).items():
                if k not in flat_equipment:
                    flat_equipment[k] = v
        if flat_equipment:
            result["equipment"] = flat_equipment

        return result

    def _extract_server_label(self, el) -> dict | None:
        try:
            if not el.get("class"):
                text = el.get_text(strip=True)
                if text.startswith("Server"):
                    return {"name": text, "sides": {}, "equipment": {}}
        except Exception as e:
            logger.exception(f"Error while extract server mark: {e}")
        return None

    def _extract_mission_item(self, el) -> dict | None:
        try:
            if el.select_one(SELECTORS["map"]):
                return {"map": el.get_text(strip=True)}
            elif el.select_one(SELECTORS["time"]):
                return {"time": el.get_text(strip=True)}
            elif el.select_one(SELECTORS["users"]):
                return {"sides": self.parse_equipment(el)}
            elif el.select_one(SELECTORS["equipment"]):
                return {"equipment": self.parse_equipment(el)}
        except Exception as e:
            logger.exception(f"Error while extracting missiong element data: {e}")
        return None

    def _process_server_data(self, el, current_server, result):
        try:
            item_data = self._extract_mission_item(el)
            if not item_data:
                return current_server

            if "map" in item_data:
                result["map"] = item_data["map"]
            if "time" in item_data:
                result["time"] = item_data["time"]

            if "sides" in item_data or "equipment" in item_data:
                if current_server is None:
                    current_server = {"name": "default", "sides": {}, "equipment": {}}
                    result["servers"].append(current_server)
                if "sides" in item_data:
                    current_server["sides"].update(item_data["sides"])
                if "equipment" in item_data:
                    current_server["equipment"].update(item_data["equipment"])
                    
        except Exception as e:
            logger.exception(f"Error while parse server data: {e}")
        return current_server

    @staticmethod
    def parse_equipment(block):
        equipment = {}
        try:
            for tag in block.find_all(True):
                for cls in tag.get("class", []):
                    if cls.endswith("-side"):
                        equipment[cls] = tag.get_text("\n", strip=True)
                        break
        except Exception as e:
            logger.exception(f"Error while parse equipment: {e}")
        return equipment

    @staticmethod
    def print_report(sections):
        for section in sections:
            logger.info("=" * 60)
            logger.info(f"SECTION: {section['title']}")

            for mission in section["missions"]:
                logger.info("-" * 40)
                logger.info(f"MISSION: {mission['name']}")
                info = mission.get("info", {})

                if info.get("map"):
                    logger.info(f"Map: {info['map']}")
                if info.get("time"):
                    logger.info(f"Time: {info['time']}")
                if info.get("description"):
                    logger.info("Description:")
                    logger.info(info["description"]["text"])
                    for link in info["description"].get("links", []):
                        logger.info(f"Link: {link}")

                if info.get("servers"):
                    for server in info["servers"]:
                        logger.info(f"SERVER: {server.get('name')}")
                        for side, val in server.get("sides", {}).items():
                            logger.info(f"{side.upper()} SIDE:")
                            logger.info(val)
                        for side, val in server.get("equipment", {}).items():
                            logger.info(f"{side.upper()} EQUIPMENT:")
                            logger.info(val)
                elif info.get("equipment"):
                    for side, eq in info.get("equipment", {}).items():
                        logger.info(f"{side.upper()} SIDE:")
                        logger.info(eq)
