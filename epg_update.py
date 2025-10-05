from datetime import datetime, timedelta

# 🕐 نحسب التاريخ الحالي (UTC)
today = datetime.utcnow()
start = today.replace(hour=0, minute=0, second=0)
stop = start + timedelta(days=1)

# نحولهم إلى تنسيق EPG (YYYYMMDDhhmmss +0000)
start_str = start.strftime("%Y%m%d%H%M%S +0000")
stop_str = stop.strftime("%Y%m%d%H%M%S +0000")

# 🧩 محتوى ملف EPG
epg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="ChatGPT EPG Generator">

  <!-- Abu Dhabi Sports -->
  <channel id="AbudhabiSports.ae@MENA">
    <display-name>Abu Dhabi Sports</display-name>
    <icon src="https://i.postimg.cc/Nj4JQMTX/Picsart-25-10-04-11-52-31-346.png" />
    <url>https://www.adsports.ae</url>
  </channel>

  <!-- SHASHA Sports -->
  <channel id="ShashaSports.kw@MENA">
    <display-name>SHASHA Sports</display-name>
    <icon src="https://i.postimg.cc/Nj4JQMTX/Picsart-25-10-04-11-52-31-346.png" />
    <url>https://www.shasha.kw</url>
  </channel>

  <!-- البرنامج اليومي لقناة أبوظبي الرياضية -->
  <programme start="{start_str}" stop="{stop_str}" channel="AbudhabiSports.ae@MENA">
    <title lang="ar">قناة الدوري الإيطالي</title>
    <desc lang="ar">يتابع عشاق كرة القدم عبر قناة أبوظبي الرياضية أقوى مباريات الدوري الإيطالي "سيري آ"، بمشاركة أعرق الأندية مثل ميلان، إنتر، يوفنتوس، وروما. تغطية شاملة تتضمن التحليل الفني، أبرز اللقطات، وآراء خبراء كرة القدم.</desc>
  </programme>

  <!-- البرنامج اليومي لقناة شاشا -->
  <programme start="{start_str}" stop="{stop_str}" channel="ShashaSports.kw@MENA">
    <title lang="ar">مباريات الدوري الإيطالي</title>
    <desc lang="ar">مباريات الدوري الإيطالي تُنقل حصريًا على قنوات شاشا الكويتية، مع تغطية مميزة لأحداث البطولة وتحليل لأداء الأندية والنجوم.</desc>
  </programme>

</tv>
'''

# 💾 حفظ الملف
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(epg_content)

print("✅ تم إنشاء epg.xml بنجاح! يحتوي على قناتين (Abu Dhabi Sports و SHASHA Sports)")
