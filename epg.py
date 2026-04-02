import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
URL = "https://www.thesportsdb.com/api/v1/json/123/eventsnextleague.php?id=4332"
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"

# التاريخ الذي تريد سحب المباريات له (مثلاً الأحد القادم)
TARGET_DATE = "2026-04-04"

# -------------------------
# طلب البيانات
# -------------------------
response = requests.get(URL)
data = response.json()
events = data.get("events", [])

tv = ET.Element("tv")

# فلترة المباريات حسب TARGET_DATE
day_events = [m for m in events if m.get("dateEvent") == TARGET_DATE]

if not day_events:
    # لا توجد مباريات → برنامج وهمي
    start_dt = datetime.strptime(TARGET_DATE + " 18:00:00", "%Y-%m-%d %H:%M:%S")
    stop_dt = start_dt + timedelta(hours=2)
    prog = ET.SubElement(tv, "programme", {
        "channel": CHANNEL_ID,
        "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
        "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
    })
    ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TITLE
else:
    for match in day_events:
        start_dt = datetime.strptime(match["dateEvent"] + " " + match["strTime"], "%Y-%m-%d %H:%M:%S")
        stop_dt = start_dt + timedelta(hours=2)
        title = f"{match['strHomeTeam']} vs {match['strAwayTeam']}"

        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = title

# -------------------------
# حفظ XML
# -------------------------
ET.ElementTree(tv).write("epg.xml", encoding="utf-8", xml_declaration=True)
print(f"تم إنشاء epg.xml ليوم {TARGET_DATE}")
