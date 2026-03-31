import feedparser
import pandas as pd
from datetime import datetime

# 1) Keywords (واسعة زي ما اتفقنا)
keywords = [
    "حادث مصر",
    "وفاة مصر",
    "غرق مصر",
    "حريق مصر",
    "سرقة مصر",
    "اصابة مصر"
]

all_news = []

# 2) سحب الأخبار
for keyword in keywords:
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ar&gl=EG&ceid=EG:ar"
    feed = feedparser.parse(url)

    for entry in feed.entries:
        all_news.append({
            "keyword": keyword,
            "العنوان": entry.title,
            "اللينك": entry.link,
            "التاريخ": entry.published
        })

# 3) DataFrame
df = pd.DataFrame(all_news)

# 4) إزالة التكرار
df.drop_duplicates(subset=["العنوان"], inplace=True)

# 5) تحديد لو الخبر له علاقة بنادي/مركز شباب
places = ["نادي", "مركز شباب"]
df["متعلق بنادي/مركز"] = df["العنوان"].str.contains('|'.join(places))

# 6) تصنيف نوع الحادث
def classify(title):
    if "غرق" in title:
        return "غرق"
    elif "حريق" in title:
        return "حريق"
    elif "سرقة" in title:
        return "سرقة"
    elif "وفاة" in title:
        return "وفاة"
    elif "إصابة" in title:
        return "اصابة"
    else:
        return "حادث"

df["نوع الحادث"] = df["العنوان"].apply(classify)

# 7) ترتيب الأعمدة
df = df[["التاريخ", "العنوان", "نوع الحادث", "متعلق بنادي/مركز", "اللينك"]]

# 8) حفظ Excel
file_name = f"incidents_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
df.to_excel(file_name, index=False)

print("تم إنشاء الملف بنجاح ✅")