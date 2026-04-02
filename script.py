import feedparser
import pandas as pd
from datetime import datetime

# RSS feed اليوم السابع قسم الحوادث
rss_url = "https://www.youm7.com/rss/section/حوادث"

# الكلمات المفتاحية للفلترة على النوادي ومراكز الشباب
places = ["نادي", "مركز شباب", "صالة رياضية"]

# تاريخ البداية
start_year = 2026
start_month = 1
start_day = 1

all_news = []

feed = feedparser.parse(rss_url)

for entry in feed.entries:
    try:
        published = datetime(*entry.published_parsed[:6])
    except Exception:
        continue

    # فلترة حسب التاريخ
    if published >= datetime(start_year, start_month, start_day):
        # فلترة الحوادث اللي فيها النوادي فقط
        title_lower = entry.title.lower()
        if any(word.lower() in title_lower for word in places):
            all_news.append({
                "التاريخ": published.strftime("%d/%m/%Y"),
                "العنوان": entry.title,
                "اللينك": entry.link
            })

# تحويل ل DataFrame وحفظ Excel
df = pd.DataFrame(all_news)
print(f"عدد الأخبار بعد التصفية: {len(df)}")
df.to_excel("youm7_incidents_clubs.xlsx", index=False)
print("تم إنشاء الملف ✅")
