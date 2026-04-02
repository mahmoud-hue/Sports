import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

all_news = []

# =========================
# 🔵 1) Youm7
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

        all_news.append({
            "المصدر": "Youm7",
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "اللينك": "https://www.youm7.com" + href
        })

# =========================
# 🟠 2) ElBalad
# =========================
print("ElBalad...")
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

        all_news.append({
            "المصدر": "ElBalad",
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "اللينك": href
        })

# =========================
# 🟢 3) Masrawy (سريع جدًا)
# =========================
print("Masrawy...")
try:
    res = requests.get("https://www.masrawy.com/news/news_cases", timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    for a in soup.find_all("a"):
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or len(title) < 20:
            continue
        if not href or "/news/" not in href:
            continue

        full_link = href if href.startswith("http") else "https://www.masrawy.com" + href

        all_news.append({
            "المصدر": "Masrawy",
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "اللينك": full_link
        })
except:
    pass

# =========================
# 🟣 4) AlWatan
# =========================
print("AlWatan...")
try:
    res = requests.get("https://www.elwatannews.com/section/115", timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    for a in soup.find_all("a"):
        title = a.get_text(strip=True)
        href = a.get("href")

        if not title or len(title) < 20:
            continue
        if not href or not href.startswith("http"):
            continue

        all_news.append({
            "المصدر": "AlWatan",
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "اللينك": href
        })
except:
    pass

# =========================
# 📊 تنظيف البيانات
# =========================
df = pd.DataFrame(all_news).drop_duplicates(subset=["العنوان"])

print("عدد الأخبار:", len(df))

df.to_excel("EGYPT_INCIDENTS_LIVE.xlsx", index=False)

print("تم إنشاء الملف ✅")
