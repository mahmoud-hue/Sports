import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

base_url = "https://www.youm7.com/Section/حوادث/203/"

places = ["نادي", "مركز شباب", "صالة", "صالة رياضية"]

all_news = []

for page in range(1, 6):
    print(f"Fetching page {page}...")
    url = base_url + str(page)

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"Error in page {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # هنا بقى بنجيب كل لينكات الأخبار بشكل عام
    links = soup.find_all("a")

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        # فلترة العناوين الحقيقية بس
        if not title or len(title) < 20:
            continue

        # لازم يكون لينك خبر
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

df.to_excel("final_incidents.xlsx", index=False)

print("تم إنشاء الملف ✅")
