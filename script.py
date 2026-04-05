import feedparser
import pandas as pd
from datetime import datetime
import urllib.parse

# ==========================
# 🔥 كلمات البحث الرئيسية (أحداث فعلية في النوادي)
queries = [
    "حادث نادي مصر",
    "حريق نادي مصر",
    "غرق نادي مصر",
    "حادث مركز شباب مصر",
    "حريق مركز شباب مصر",
    "إصابة مركز شباب مصر",
    "حادث ملعب مصر"
]

# ==========================
# ❌ كلمات نستبعدها (نعي/تعزية/تكريم...)
exclude_words = ["تعزية", "وفاة لاعب", "تكريم", "نعي", "ذكرى", "تكريم"]

# ==========================
all_news = []
start_date = datetime(2026, 1, 1)

# ==========================
for q in queries:
    encoded = urllib.parse.quote(q)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=ar&gl=EG&ceid=EG:ar"
    feed = feedparser.parse(url)

    print(f"جارٍ فتح الأخبار لـ: {q} ... عدد الأخبار: {len(feed.entries)}")

    for entry in feed.entries:
        if hasattr(entry, "published_parsed"):
            date = datetime(*entry.published_parsed[:6])
        else:
            continue

        # فلترة حسب التاريخ
        if date >= start_date:
            title = entry.title

            # فلترة حسب الكلمات المستبعدة
            if not any(word in title for word in exclude_words):
                all_news.append({
                    "التاريخ": date.strftime("%Y-%m-%d"),
                    "العنوان": title,
                    "اللينك": entry.link
                })

# ==========================
df = pd.DataFrame(all_news)
df.drop_duplicates(inplace=True)

print("عدد الأخبار الدقيقة:", len(df))

# ==========================
file_name = f"news_precise_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
df.to_excel(file_name, index=False)

print(f"تم إنشاء الملف بنجاح ✅: {file_name}")
