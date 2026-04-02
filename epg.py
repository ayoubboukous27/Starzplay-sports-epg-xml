import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
API_KEY = "123"
LEAGUE_ID = "4332"  # Serie A
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"

# -------------------------
# سحب المباريات القادمة
# -------------------------
url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsnextleague.php?id={LEAGUE_ID}"
response = requests.get(url)
data = response.json()
events = data.get("events", [])

# -------------------------
# بناء XMLTV
# -------------------------
tv = ET.Element("tv")

if not events:
    # برنامج وهمي
    start_dt = datetime.utcnow()
    stop_dt = start_dt + timedelta(hours=2)
    prog = ET.SubElement(tv, "programme", {
        "channel": CHANNEL_ID,
        "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
        "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
    })
    ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TITLE
else:
    for match in events:
        date_event = match.get("dateEvent")
        time_event = match.get("strTime", "18:00:00")
        start_dt = datetime.strptime(date_event + " " + time_event, "%Y-%m-%d %H:%M:%S")
        stop_dt = start_dt + timedelta(hours=2)
        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = match.get("strEvent", "Unknown Match")

# -------------------------
# حفظ الملف
# -------------------------
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
print("تم إنشاء epg.xml بنجاح")
