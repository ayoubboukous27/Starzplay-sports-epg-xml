import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
API_KEY = "eaa0f8c7fa0765ecc6a7f3f8f753699a"
LEAGUE_ID = 135   # Serie A
SEASON_ID = 7286  # الموسم الحالي
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"

HEADERS = {
    "x-apisports-key": API_KEY
}

tv = ET.Element("tv")

# تغطية 7 أيام قادمة
for day_offset in range(7):
    date_obj = datetime.utcnow() + timedelta(days=day_offset)
    date_str = date_obj.strftime("%Y-%m-%d")

    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "league": LEAGUE_ID,
        "season": 2025,  # السنة نفسها أو يمكن تجاهل إذا API يعتمد season ID
        "date": date_str
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    events = data.get("response", [])

    # البحث عن مباريات الموسم المحدد فقط
    day_events = []
    for match in events:
        if match["league"]["id"] == LEAGUE_ID:
            day_events.append(match)

    if not day_events:
        # لا توجد مباريات → برنامج وهمي
        start_dt = datetime.combine(date_obj.date(), datetime.min.time()) + timedelta(hours=18)
        stop_dt = start_dt + timedelta(hours=2)
        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TITLE
    else:
        for match in day_events:
            fixture = match["fixture"]
            teams = match["teams"]
            date_event = fixture["date"][:10]  # YYYY-MM-DD
            time_event = fixture["date"][11:19]  # HH:MM:SS
            start_dt = datetime.strptime(date_event + " " + time_event, "%Y-%m-%d %H:%M:%S")
            stop_dt = start_dt + timedelta(hours=2)

            prog = ET.SubElement(tv, "programme", {
                "channel": CHANNEL_ID,
                "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
                "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
            })
            ET.SubElement(prog, "title").text = f"{teams['home']['name']} vs {teams['away']['name']}"

# -------------------------
# حفظ XML
# -------------------------
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

print("تم إنشاء epg.xml يغطي 7 أيام مع البرنامج الوهمي عند عدم وجود مباريات")
