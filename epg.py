import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
API_KEY = "509ceffac75b4189b4c0e129e35941bb"
COMPETITION = "SA"  # Serie A
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"
NUM_DAYS = 7  # الأيام القادمة التي نريد إنشاء EPG لها

HEADERS = {"X-Auth-Token": API_KEY}

# -------------------------
# سحب جميع المباريات القادمة
# -------------------------
url = f"https://api.football-data.org/v4/competitions/{COMPETITION}/matches?status=SCHEDULED"
response = requests.get(url, headers=HEADERS)
data = response.json()
matches = data.get("matches", [])

# -------------------------
# بناء XMLTV
# -------------------------
tv = ET.Element("tv")

today = datetime.utcnow()

for day_offset in range(NUM_DAYS):
    current_date = today + timedelta(days=day_offset)
    date_str = current_date.strftime("%Y-%m-%d")

    # فلترة المباريات لليوم الحالي
    day_matches = [m for m in matches if m["utcDate"].startswith(date_str)]
    
    # ترتيب المباريات حسب الوقت
    day_matches.sort(key=lambda m: m["utcDate"])

    if not day_matches:
        # برنامج وهمي من 18:00 إلى 20:00 UTC
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
# حفظ الملف بشكل منظم
# -------------------------
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

print(f"تم إنشاء epg.xml منظم لفترة {NUM_DAYS} أيام القادمة للـ Serie A")
