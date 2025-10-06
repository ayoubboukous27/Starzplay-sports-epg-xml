from datetime import datetime, timedelta

# نحسب التاريخ الحالي (UTC)
today = datetime.utcnow()
start = today.replace(hour=0, minute=0, second=0)
stop = start + timedelta(days=1)

# نحولهم إلى تنسيق EPG (YYYYMMDDhhmmss +0000)
start_str = start.strftime("%Y%m%d%H%M%S +0000")
stop_str = stop.strftime("%Y%m%d%H%M%S +0000")

# محتوى ملف EPG
epg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="ChatGPT EPG Generator">

  <channel id="AbudhabiSports.ae@MENA">
    <display-name>Abu Dhabi Sports</display-name>
    <icon src="https://i.postimg.cc/Nj4JQMTX/Picsart-25-10-04-11-52-31-346.png" />
    <url>https://www.adsports.ae</url>
  </channel>

  <channel id="ShashaSports.kw@MENA">
    <display-name>SHASHA Sports</display-name>
    <icon src="https://i.postimg.cc/Y0VGd3cw/Picsart-25-10-05-20-04-57-624.png" />
    <url>https://www.shasha.kw</url>
  </channel>

  <channel id="Thmanya.sa@MENA">
    <display-name>Thmanya</display-name>
    <icon src="https://iili.io/KhlVFeI.png" />
    <url>https://www.thmanyah.com</url>
  </channel>

  <channel id="AsharqDocumentary.sa@MENA">
    <display-name>Asharq Documentary</display-name>
    <icon src="https://iili.io/KhlV35N.png" />
    <url>https://www.asharqdocumentary.com</url>
  </channel>

  <channel id="AsharqDiscovery.sa@MENA">
    <display-name>Asharq Discovery</display-name>
    <icon src="https://iili.io/KhlV2Jp.png" />
    <url>https://www.asharqdiscovery.com</url>
  </channel>

  <programme start="{start_str}" stop="{stop_str}" channel="AbudhabiSports.ae@MENA">
    <title lang="ar">قناة الدوري الإيطالي</title>
    <desc lang="ar">يتابع عشاق كرة القدم عبر قناة أبوظبي الرياضية أقوى مباريات الدوري الإيطالي "سيري آ"، بمشاركة أعرق الأندية مثل ميلان، إنتر، يوفنتوس، وروما. تغطية شاملة تتضمن التحليل الفني، أبرز اللقطات، وآراء خبراء كرة القدم.</desc>
  </programme>

  <programme start="{start_str}" stop="{stop_str}" channel="ShashaSports.kw@MENA">
    <title lang="ar">مباريات الدوري الإيطالي</title>
    <desc lang="ar">مباريات الدوري الإيطالي تُنقل حصريًا على قنوات شاشا الكويتية، مع تغطية مميزة لأحداث البطولة وتحليل لأداء الأندية والنجوم.</desc>
  </programme>

  <programme start="{start_str}" stop="{stop_str}" channel="Thmanya.sa@MENA">
    <title lang="ar">نقل مباريات الدوري السعودي حصريا</title>
    <desc lang="ar">متابعة حصرية وشاملة لأهم مباريات الدوري السعودي للمحترفين، مع تغطية مميزة وتحليل فني عميق لأداء الفرق والنجوم.</desc>
  </programme>

  <programme start="{start_str}" stop="{stop_str}" channel="AsharqDocumentary.sa@MENA">
    <title lang="ar">وثائقيات تاريخية وثقافية</title>
    <desc lang="ar">رحلة عبر التاريخ والحضارة العربية، مع برامج وأفلام وثائقية معمقة عن أهم الأحداث والشخصيات التاريخية التي شكلت المنطقة.</desc>
  </programme>

  <programme start="{start_str}" stop="{stop_str}" channel="AsharqDiscovery.sa@MENA">
    <title lang="ar">برامج عن الطبيعة والعلوم</title>
    <desc lang="ar">اكتشف أسرار العالم من خلال مجموعة من البرامج الوثائقية المثيرة التي تغطي مواضيع عن الطبيعة، الفضاء، والتكنولوجيا، مترجمة إلى العربية.</desc>
  </programme>

</tv>
'''

# حفظ الملف
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(epg_content)

print("✅ تم تحديث epg.xml بنجاح! تم تصحيح الشعارات وإضافة البرامج المطلوبة.")
