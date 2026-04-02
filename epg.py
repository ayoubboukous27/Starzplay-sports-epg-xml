import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

API_KEY = "123"
LEAGUE_ID = "4332"
CHANNEL_ID = "seriea"
DEFAULT_PROGRAM_TITLE = "No Match Today - Studio"

tv = ET.Element("tv")

for day_offset in range(7):
    date_obj = datetime.utcnow() + timedelta(days=day_offset)
    # نستخدم eventsnextleague.php مرة واحدة لسحب المباريات القادمة
    url = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/eventsnextleague.php?id={LEAGUE_ID}"
    response = requests.get(url)
    data = response.json()
    events = data.get("events", [])

    found_match = False
    for match in events:
        # فقط مباريات اليوم الحالي في الدورة
        date_event = match.get("dateEvent")
        if date_event != date_obj.strftime("%Y-%m-%d"):
            continue
        found_match = True
        time_event = match.get("strTime", "18:00:00")
        start_dt = datetime.strptime(date_event + " " + time_event, "%Y-%m-%d %H:%M:%S")
        stop_dt = start_dt + timedelta(hours=2)
        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = match.get("strEvent", "Unknown Match")

    if not found_match:
        # إنشاء برنامج وهمي
        start_dt = datetime.combine(date_obj.date(), datetime.min.time()) + timedelta(hours=18)
        stop_dt = start_dt + timedelta(hours=2)
        prog = ET.SubElement(tv, "programme", {
            "channel": CHANNEL_ID,
            "start": start_dt.strftime("%Y%m%d%H%M%S +0000"),
            "stop": stop_dt.strftime("%Y%m%d%H%M%S +0000")
        })
        ET.SubElement(prog, "title").text = DEFAULT_PROGRAM_TITLE

ET.ElementTree(tv).write("epg.xml", encoding="utf-8", xml_declaration=True)
print("تم إنشاء epg.xml يغطي 7 أيام بنجاح")
