import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

base_url = "https://www.youm7.com/Section/حوادث/203/"

all_news = []

# آخر شهرين
two_months_ago = datetime.now() - timedelta(days=60)

page = 1

while True:
    print(f"Page {page}")

    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("h3")

    if not items:
        break

    for item in items:
        a_tag = item.find("a")

        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = "https://www.youm7.com" + a_tag.get("href")

            # فلتر النوادي ومراكز الشباب
            if "نادي" in title or "مركز شباب" in title:
                all_news.append({
                    "العنوان": title,
                    "اللينك": link
                })

    # وقف بعد 5 صفحات (مبدئيًا عشان الأداء)
    if page == 5:
        break

    page += 1

df = pd.DataFrame(all_news)

print("عدد الأخبار:", len(df))

df.to_excel("youm7_filtered.xlsx", index=False)

print("تم إنشاء الملف ✅")
