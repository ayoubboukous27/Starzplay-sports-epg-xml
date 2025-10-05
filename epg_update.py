from datetime import datetime, timedelta

# نحسب التاريخ الحالي (UTC)
today = datetime.utcnow()
start = today.replace(hour=0, minute=0, second=0)
stop = start + timedelta(days=1)

# نحولهم إلى تنسيق EPG (YYYYMMDDhhmmss +0000)
start_str = start.strftime("%Y%m%d%H%M%S +0000")
stop_str = stop.strftime("%Y%m%d%H%M%S +0000")

# نص الـ EPG
epg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="ChatGPT EPG Generator">

  <!-- Abu Dhabi Sports -->
  <channel id="AbudhabiSports.ae@MENA">
    <display-name>Abu Dhabi Sports</display-name>
    <icon src="https://i.postimg.cc/Nj4JQMTX/Picsart-25-10-04-11-52-31-346.png" />
    <url>https://www.adsports.ae</url>
  </channel>

  <!-- البرنامج -->
  <programme start="{start_str}" stop="{stop_str}" channel="AbudhabiSports.ae@MENA">
    <title lang="ar">قناة الدوري الإيطالي</title>
    <desc lang="ar">نقل مباشر وتحليلات لمباريات الدوري الإيطالي على قناة أبوظبي الرياضية.</desc>
  </programme>

</tv>
'''

# نحفظ الملف
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(epg_content)

print("✅ تم إنشاء epg.xml بنجاح!")
