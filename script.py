import feedparser
import pandas as pd
from datetime import datetime
import urllib.parse  # لحل مشاكل URL

# 1️⃣ Keywords لـ Google News فقط
keywords = ["حادث", "وفاة", "غرق", "حريق", "سرقة", "إصابة"]

# 2️⃣ RSS sources كاملة
rss_feeds = [
    # اليوم السابع (قسم الحوادث)
    "https://www.youm7.com/rss/section/1/0/1/1",
    # مصراوي (الحوادث)
    "https://www.masrawy.com/rss/section/0/1/0",
    # الوطن (الحوادث)
    "https://www.elwatannews.com/rss",
    # فيتو (الحوادث)
    "https://www.vetogate.com/rss/section/12",
    # الدستور (الحوادث)
    "https://www.dostor.org/rsssection/3"
]

all_news = []

# 3️⃣ سحب أخبار Google News حسب keywords
for keyword in keywords:
    safe_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={safe_keyword}+مصر&hl=ar&gl=EG&ceid=EG:ar"
    feed = feedparser.parse(url)
    for entry in feed.entries:
        all_news.append({
            "المصدر": "Google News",
            "العنوان": entry.title,
            "اللينك": urllib.parse.quote(entry.link, safe=':/?=&'),
            "التاريخ": entry.published if "published" in entry else datetime.now().strftime("%Y-%m-%d")
        })

# 4️⃣ سحب الأخبار من باقي المصادر
for url in rss_feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        all_news.append({
            "المصدر": url,
            "العنوان": entry.title,
            "اللينك": urllib.parse.quote(entry.link, safe=':/?=&'),
            "التاريخ": entry.published if "published" in entry else datetime.now().strftime("%Y-%m-%d")
        })

# 5️⃣ إنشاء DataFrame
df = pd.DataFrame(all_news)

# 6️⃣ إزالة التكرار
df.drop_duplicates(subset=["العنوان"], inplace=True)

# 🔹 بدون أي فلترة، نجرب نشوف الأخبار
print("عدد الأخبار المجمعة:", len(df))
print("أول 20 خبر:")
print(df.head(20))

# 7️⃣ ترتيب الأعمدة
df = df[["المصدر", "التاريخ", "العنوان", "اللينك"]]

# 8️⃣ حفظ Excel لتجربة
file_name = "test_incidents.xlsx"
df.to_excel(file_name, index=False)

print("تم إنشاء الملف التجريبي بنجاح ✅")
