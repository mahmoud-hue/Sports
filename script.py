import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

base_url = "https://www.youm7.com/Section/حوادث/203/"

all_news = []
places = ["نادي", "مركز شباب"]

# 5 صفحات بدل 3
for page in range(1, 6):
    print(f"جاري فتح الصفحة {page}...")

    url = base_url + str(page)
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("h3")

    if not items:
        break

    for item in items:
        a_tag = item.find("a")

        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = "https://www.youm7.com" + a_tag.get("href")

            if any(word in title for word in places):
                all_news.append({
                    "التاريخ": datetime.now().strftime("%d/%m/%Y"),
                    "العنوان": title,
                    "اللينك": link
                })

df = pd.DataFrame(all_news)

print("عدد الأخبار:", len(df))

df.to_excel("youm7_filtered_fast.xlsx", index=False)

print("تم إنشاء الملف ✅")
