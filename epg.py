import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# -------------------------
# الإعدادات
# -------------------------
API_KEY = "123"
LEAGUE_ID = "4332"           # Serie A
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"  # برنامج وهمي

# -------------------------
# بناء XMLTV
# -------------------------
tv = ET.Element("tv")

# تغطية 7 أيام قادمة
for day_offset in range(7):
    date_obj = datetime.utcnow() + timedelta(days=day_offset)
    date_str = date_obj.strftime("%Y-%m-%d")

    # سحب المباريات لهذا اليوم
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsday.php?d={date_str}"
    response = requests.get(url)
    data = response.json()
    events = data.get("events", [])

    if not events:
        # لا توجد مباريات → برنامج وهمي لمدة ساعتين
        start_dt = datetime.combine(date_obj.date(), datetime.min.time()) + timedelta(hours=18)  # 18:00 UTC
        stop_dt = start_dt + timedelta(hours=2)

        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TITLE

    else:
        for match in events:
            if match.get("idLeague") != LEAGUE_ID:
                continue  # تجاهل المباريات غير Serie A

            date_event = match.get("dateEvent")
            time_event = match.get("strTime", "18:00:00")
            start_dt = datetime.strptime(date_event + " " + time_event, "%Y-%m-%d %H:%M:%S")
            stop_dt = start_dt + timedelta(hours=2)  # نفترض كل مباراة مدتها ساعتين

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

print("تم إنشاء epg.xml يغطي 7 أيام بنجاح")
