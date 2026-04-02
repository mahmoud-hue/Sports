import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time

base_url = "https://www.youm7.com/Section/حوادث/203/"

# كلمات موسعة
places = [
    "نادي", "نوادي", "مركز شباب",
    "استاد", "ستاد", "ملعب",
    "صالة", "صالة مغطاة",
    "أكاديمية", "وزارة الشباب"
]

# آخر 10 أيام
limit_date = datetime.now() - timedelta(days=10)

all_news = []

for page in range(1, 6):
    print(f"Page {page}")
    url = base_url + str(page)

    try:
        res = requests.get(url, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
    except:
        continue

    links = soup.find_all("a")

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or len(title) < 20:
            continue

        if not href or "/story/" not in href:
            continue

        full_link = "https://www.youm7.com" + href

        # ندخل الخبر نجيب التاريخ
        try:
            article_res = requests.get(full_link, timeout=15)
            article_soup = BeautifulSoup(article_res.text, "html.parser")

            date_tag = article_soup.find("span", class_="date")
            if not date_tag:
                continue

            date_text = date_tag.text.strip()

            # مثال: "السبت، 30 مارس 2026 02:00 م"
            published = datetime.strptime(date_text.split("،")[-1].strip(), "%d %B %Y %I:%M %p")

        except:
            continue

        # وقف لو أقدم من 10 أيام
        if published < limit_date:
            print("وقفنا عشان عدى 10 أيام 👌")
            break

        related = any(word in title for word in places)

        all_news.append({
            "التاريخ": published.strftime("%d/%m/%Y"),
            "العنوان": title,
            "متعلق بنادي/مركز": related,
            "اللينك": full_link
        })

        time.sleep(0.5)  # مهم عشان متعملش block

# DataFrame
df = pd.DataFrame(all_news).drop_duplicates(subset=["العنوان"])

print("عدد الأخبار:", len(df))

df.to_excel("incidents_10days.xlsx", index=False)

print("تم إنشاء الملف ✅")
