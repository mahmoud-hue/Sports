import feedparser
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse  # مهم لتحويل الكلمات العربية في URL

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
            "العنوان": entry.title,
            "اللينك": urllib.parse.quote(entry.link, safe=':/?=&'),
            "التاريخ": entry.published if "published" in entry else datetime.now().strftime("%Y-%m-%d")
        })

# 4️⃣ سحب الأخبار من باقي المصادر
for url in rss_feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        all_news.append({
            "العنوان": entry.title,
            "اللينك": urllib.parse.quote(entry.link, safe=':/?=&'),
            "التاريخ": entry.published if "published" in entry else datetime.now().strftime("%Y-%m-%d")
        })

# 5️⃣ إنشاء DataFrame
df = pd.DataFrame(all_news)

# 6️⃣ إزالة التكرار
df.drop_duplicates(subset=["العنوان"], inplace=True)

# 7️⃣ تصنيف نوع الحادث
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
        return "إصابة"
    else:
        return None  # مش حادث

df["نوع الحادث"] = df["العنوان"].apply(classify)

# 8️⃣ تصفية الأخبار الحقيقية المرتبطة بالنوادي أو مراكز الشباب
places = ["نادي", "مركز شباب"]
df = df[df["نوع الحادث"].notna()]  # اخبار حقيقية فقط
df = df[df["العنوان"].str.contains('|'.join(places))]  # النوادي أو مراكز الشباب

# 9️⃣ تصفية أخبار اليوم السابق فقط
yesterday = datetime.now() - timedelta(days=1)
df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
df = df[df['التاريخ'].dt.date == yesterday.date()]

# 🔟 ترتيب الأعمدة
df = df[["التاريخ", "العنوان", "نوع الحادث", "اللينك"]]

# 1️⃣1️⃣ حفظ Excel
file_name = "incidents.xlsx"
df.to_excel(file_name, index=False)

print("تم إنشاء الملف بنجاح ✅")
