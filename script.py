import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import feedparser

all_news = []

# كلمات مفتاحية موسعة
places = [
    "نادي", "نوادي", "مركز شباب",
    "استاد", "ستاد", "ملعب",
    "صالة", "صالة مغطاة",
    "أكاديمية", "وزارة الشباب",
    "الأهلي", "الزمالك"
]

# =========================
# 🟢 1) Google News (RSS)
# =========================
print("Google News...")

rss_url = "https://news.google.com/rss/search?q=حادث+مصر&hl=ar&gl=EG&ceid=EG:ar"
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    title = entry.title
    link = entry.link

    related = any(word in title for word in places)

    all_news.append({
        "المصدر": "Google",
        "التاريخ": datetime.now().strftime("%d/%m/%Y"),
        "العنوان": title,
        "متعلق بنادي/مركز": related,
        "اللينك": link
    })

# =========================
# 🔵 2) Youm7 (Scraping)
# =========================
print("Youm7...")

for page in range(1, 6):
    url = f"https://www.youm7.com/Section/حوادث/203/{page}"

    try:
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
    except:
        continue

    for a in soup.find_all("a"):
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or len(title) < 20:
            continue

        if not href or "/story/" not in href:
            continue

        full_link = "https://www.youm7.com" + href

        related = any(word in title for word in places)

        all_news.append({
            "المصدر": "Youm7",
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "متعلق بنادي/مركز": related,
            "اللينك": full_link
        })

# =========================
# 🟠 3) Sada ElBalad (Scraping)
# =========================
print("Sada ElBalad...")

for page in range(1, 4):
    url = f"https://www.elbalad.news/Section/195/{page}"

    try:
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
    except:
        continue

    for a in soup.find_all("a"):
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or len(title) < 20:
            continue

        if not href or not href.startswith("http"):
            continue

        related = any(word in title for word in places)

        all_news.append({
            "المصدر": "ElBalad",
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "متعلق بنادي/مركز": related,
            "اللينك": href
        })

# =========================
# 📊 تنظيف البيانات
# =========================
df = pd.DataFrame(all_news)

# إزالة التكرار
df = df.drop_duplicates(subset=["العنوان"])

print("عدد الأخبار:", len(df))
print("عدد True:", df["متعلق بنادي/مركز"].sum())

# حفظ
df.to_excel("FINAL_NEWS.xlsx", index=False)

print("تم إنشاء الملف ✅")
