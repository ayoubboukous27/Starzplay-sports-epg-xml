import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
API_KEY = "509ceffac75b4189b4c0e129e35941bb"
COMPETITION = "SA"  # Serie A
CHANNEL_ID = "starzplay"  # هذا هو id القناة في XMLTV
CHANNEL_NAME = "Starz Play"
NUM_DAYS = 7
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"

HEADERS = {"X-Auth-Token": API_KEY}

# -------------------------
# سحب المباريات القادمة
# -------------------------
url = f"https://api.football-data.org/v4/competitions/{COMPETITION}/matches?status=SCHEDULED"
response = requests.get(url, headers=HEADERS)
data = response.json()
matches = data.get("matches", [])

# -------------------------
# إنشاء ملف XMLTV
# -------------------------
tv = ET.Element("tv")

# تعريف القناة
channel = ET.SubElement(tv, "channel", id=CHANNEL_ID)
ET.SubElement(channel, "display-name").text = CHANNEL_NAME

today = datetime.utcnow()

for day_offset in range(NUM_DAYS):
    current_date = today + timedelta(days=day_offset)
    date_str = current_date.strftime("%Y-%m-%d")

    # فلترة المباريات لهذا اليوم
    day_matches = [m for m in matches if m["utcDate"].startswith(date_str)]
    day_matches.sort(key=lambda m: m["utcDate"])  # ترتيب حسب الوقت

    if not day_matches:
        # برنامج وهمي 18:00 - 20:00 UTC
        start_dt = datetime.combine(current_date.date(), datetime.min.time()) + timedelta(hours=18)
        stop_dt = start_dt + timedelta(hours=2)
        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TITLE
    else:
        for match in day_matches:
            start_dt = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
            stop_dt = start_dt + timedelta(hours=2)
            title = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}"

            prog = ET.SubElement(tv, "programme", {
                "channel": CHANNEL_ID,
                "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
                "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
            })
            ET.SubElement(prog, "title").text = title

# -------------------------
# حفظ XML
# -------------------------
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

print(f"تم إنشاء epg.xml لقناة {CHANNEL_NAME} لجميع الأيام القادمة")
