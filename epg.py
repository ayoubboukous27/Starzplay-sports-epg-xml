import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"

# TheSportsDB endpoint
BASE_URL = "https://www.thesportsdb.com/api/v1/json/123/eventsnextleague.php?id=4332"

# عدد الأيام التي تريد فحصها
NUM_DAYS = 7  # يمكن تغييره حسب الحاجة
START_DATE = datetime(2025, 4, 2)  # بداية الفحص

tv = ET.Element("tv")

# -------------------------
# فحص كل يوم على حدة
# -------------------------
for day_offset in range(NUM_DAYS):
    current_date = START_DATE + timedelta(days=day_offset)
    date_str = current_date.strftime("%Y-%m-%d")

    # طلب المباريات القادمة من TheSportsDB
    response = requests.get(BASE_URL)
    data = response.json()
    events = data.get("events", [])

    # البحث عن مباريات هذا اليوم
    day_events = [m for m in events if m.get("dateEvent") == date_str]

    if not day_events:
        # لا توجد مباريات → برنامج وهمي 18:00 - 20:00 UTC
        start_dt = datetime.combine(current_date.date(), datetime.min.time()) + timedelta(hours=18)
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
            stop_dt = start_dt + timedelta(hours=2)  # نفترض كل مباراة ساعتين

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
print(f"تم إنشاء epg.xml لفترة {START_DATE.strftime('%Y-%m-%d')} + {NUM_DAYS} أيام")
