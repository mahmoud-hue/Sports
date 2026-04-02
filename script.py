import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

base_url = "https://www.youm7.com/Section/حوادث/203/"

all_news = []

# تاريخ من شهرين
two_months_ago = datetime.now() - timedelta(days=60)

page = 1

while True:
    print(f"جاري سحب الصفحة {page}...")

    url = base_url + str(page)
    response = requests.get(url)
    
    if response.status_code != 200:
        print("فشل تحميل الصفحة")
        break

    soup = BeautifulSoup(response.content, "html.parser")

    articles = soup.find_all("div", class_="story")

    if not articles:
        print("مفيش أخبار تاني")
        break

    stop = False

    for article in articles:
        try:
            title_tag = article.find("h3")
            link_tag = article.find("a")
            date_tag = article.find("span", class_="time")

            title = title_tag.text.strip() if title_tag else ""
            link = "https://www.youm7.com" + link_tag.get("href") if link_tag else ""
            date_text = date_tag.text.strip() if date_tag else ""

            # تحويل التاريخ
            date = datetime.strptime(date_text, "%d/%m/%Y")

            # وقف عند آخر شهرين
            if date < two_months_ago:
                stop = True
                break

            all_news.append({
                "التاريخ": date,
                "العنوان": title,
                "اللينك": link
            })

        except:
            continue

    if stop:
        print("وصلنا لأخبار أقدم من شهرين، وقفنا")
        break

    page += 1


# تحويل لـ DataFrame
df = pd.DataFrame(all_news)

print("عدد الأخبار:", len(df))

# حفظ Excel
df.to_excel("youm7_incidents.xlsx", index=False)

print("تم إنشاء الملف بنجاح ✅")
