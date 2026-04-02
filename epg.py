import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
API_KEY = "509ceffac75b4189b4c0e129e35941bb"
COMPETITION = "SA"  # Serie A

NUM_DAYS = 20  # عدد الأيام القادمة
CHANNELS = [
    {"id": "starzplay1", "name": "Starzplay 1", "logo": "https://raw.githubusercontent.com/ayoubboukous27/Starzplay-sports-epg-xml/refs/heads/main/Logos/starz1.png"},
    {"id": "starzplay2", "name": "Starzplay 2", "logo": "https://raw.githubusercontent.com/ayoubboukous27/Starzplay-sports-epg-xml/refs/heads/main/Logos/starz2.png"},
    {"id": "starzplay3", "name": "Starzplay 3", "logo": "https://raw.githubusercontent.com/ayoubboukous27/Starzplay-sports-epg-xml/refs/heads/main/Logos/starz3.png"}
]

DEFAULT_PROGRAM_TEMPLATE = "Serie A Highlights, Analysis, and Expert Commentary"

HEADERS = {"X-Auth-Token": API_KEY}

# -------------------------
# سحب جميع المباريات القادمة
# -------------------------
url = f"https://api.football-data.org/v4/competitions/{COMPETITION}/matches?status=SCHEDULED"
response = requests.get(url, headers=HEADERS)
data = response.json()
matches = data.get("matches", [])

# -------------------------
# إنشاء XMLTV
# -------------------------
tv = ET.Element("tv")

# تعريف القنوات
for ch in CHANNELS:
    channel = ET.SubElement(tv, "channel", id=ch["id"])
    ET.SubElement(channel, "display-name").text = ch["name"]
    ET.SubElement(channel, "icon", src=ch["logo"])

# بدء اليوم الحالي
today = datetime.utcnow()

# -------------------------
# بناء البرامج اليومية لكل قناة
# -------------------------
for day_offset in range(NUM_DAYS):
    current_date = today + timedelta(days=day_offset)
    date_str = current_date.strftime("%Y-%m-%d")

    # فلترة المباريات لهذا اليوم
    day_matches = [m for m in matches if m["utcDate"].startswith(date_str)]
    day_matches.sort(key=lambda m: m["utcDate"])  # ترتيب حسب الوقت

    for ch in CHANNELS:
        if day_matches:
            for match in day_matches:
                start_dt = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
                stop_dt = start_dt + timedelta(hours=2)
                title = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']} - Serie A Live"

                prog = ET.SubElement(tv, "programme", {
                    "channel": ch["id"],
                    "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
                    "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
                })
                ET.SubElement(prog, "title").text = title
                ET.SubElement(prog, "desc").text = f"Live broadcast of {match['homeTeam']['name']} vs {match['awayTeam']['name']} in Serie A."
        else:
            # إذا لا توجد مباريات، برنامج وهمي كل ساعة من 18:00 إلى 23:00
            for hour in range(18, 24):
                start_dt = datetime.combine(current_date.date(), datetime.min.time()) + timedelta(hours=hour)
                stop_dt = start_dt + timedelta(hours=1)
                prog = ET.SubElement(tv, "programme", {
                    "channel": ch["id"],
                    "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
                    "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
                })
                ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TEMPLATE
                ET.SubElement(prog, "desc").text = (
                    f"Comprehensive coverage of the Italian Serie A. "
                    f"Highlights, analysis, and expert commentary for {ch['name']}."
                )

# -------------------------
# حفظ XML
# -------------------------
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

print(f"تم إنشاء epg.xml لمدة {NUM_DAYS} أيام مع 3 قنوات Starzplay")
