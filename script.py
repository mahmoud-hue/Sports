import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

base_url = "https://www.youm7.com/Section/حوادث/203/"

# كلمات موسعة جامد
places = [
    "نادي", "نوادي", "مركز شباب",
    "استاد", "ستاد", "ملعب",
    "صالة", "صالة مغطاة",
    "أكاديمية", "وزارة الشباب",
    "الاهلي", "الزمالك"
]

all_news = []

# نزود الصفحات براحتنا هنا (سريع)
for page in range(1, 11):  # 10 صفحات
    print(f"Page {page}")

    url = base_url + str(page)

    try:
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, "html.parser")
    except:
        continue

    links = soup.find_all("a")

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        # فلترة العناوين الحقيقية
        if not title or len(title) < 20:
            continue

        if not href or "/story/" not in href:
            continue

        full_link = "https://www.youm7.com" + href

        related = any(word in title for word in places)

        all_news.append({
            "التاريخ": datetime.now().strftime("%d/%m/%Y"),
            "العنوان": title,
            "متعلق بنادي/مركز": related,
            "اللينك": full_link
        })

# إزالة التكرار
df = pd.DataFrame(all_news).drop_duplicates(subset=["العنوان"])

print("عدد الأخبار:", len(df))
print("عدد True:", df["متعلق بنادي/مركز"].sum())

df.to_excel("FAST_incidents.xlsx", index=False)

print("تم إنشاء الملف ✅")
