import html as _html
from core.config import SIDE_EMOJI

class Formatter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def format_mission(missions, idx: int, announcement_title: str | None = None) -> str:
        m = missions[idx]
        name = m.get("name", "Неизвестно")
        info = m.get("info", {})

        parts: list[str] = []

        def esc(text: str) -> str:
            return _html.escape(text or "")

        def side_emoji(side: str, default: str) -> str:
            side_l = side.lower()
            return next((e for k, e in SIDE_EMOJI.items() if k in side_l), default)

        def add_header(text: str):
            parts.append(text)

        def add_lines(lines: list[str]):
            parts.extend(lines)

        def format_sides(sides: dict[str, str]):
            for side, val in sides.items():
                emoji = side_emoji(side, "⚪")
                lines = [l.strip() for l in val.split("\n") if l.strip()]
                if not lines:
                    continue
                main = lines[0]
                if len(lines) > 1:
                    add_lines([f"{emoji}{esc(main)} — ⚔️ Атака"])
                else:
                    add_lines([f"{emoji}{esc(main)}"])

        def format_equipment(equipment: dict[str, str]):
            for side, val in equipment.items():
                emoji = side_emoji(side, "📦")
                add_lines([f"\n{emoji} <b>Техника:</b>", esc(val)])

        if announcement_title:
            add_header(f"📢 <b>{esc(announcement_title)}</b>\n")

        add_header(f"🎯 <b>Миссия:</b> {esc(name)}\n")

        if info.get("map"):
            add_header(f"🗺 <b>Карта:</b> {esc(info['map'])}")
        if info.get("time"):
            add_header(f"☁️ <b>Погода и время:</b> {esc(info['time'])}")

        if info.get("description"):
            add_header("\n📝 <b>Описание:</b>")
            add_header(esc(info["description"].get("text", "")))

        for srv in info.get("servers", []):
            add_header(f"\n🖥 <b>{esc(srv.get('name', 'Сервер'))}\n</b>")
            format_sides(srv.get("sides", {}))
            format_equipment(srv.get("equipment", {}))

        return "\n".join(parts)
