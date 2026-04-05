import feedparser
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

# 🔥 كلمات البحث
queries = [
    "حادث نادي مصر",
    "حريق نادي مصر",
    "غرق نادي مصر",
    "حادث مركز شباب مصر",
    "حريق مركز شباب مصر"
]

all_news = []

# 🧠 تاريخ من أول 2026
start_date = datetime(2026, 1, 1)

for q in queries:
    encoded = urllib.parse.quote(q)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=ar&gl=EG&ceid=EG:ar"

    feed = feedparser.parse(url)

    for entry in feed.entries:
        # نحاول نقرأ التاريخ
        if hasattr(entry, "published_parsed"):
            date = datetime(*entry.published_parsed[:6])
        else:
            continue

        # فلترة من 2026
        if date >= start_date:
            all_news.append({
                "التاريخ": date.strftime("%Y-%m-%d"),
                "العنوان": entry.title,
                "اللينك": entry.link
            })

df = pd.DataFrame(all_news)
df.drop_duplicates(inplace=True)

print("عدد الأخبار:", len(df))

df.to_excel("final_news.xlsx", index=False)

print("تم ✅")
