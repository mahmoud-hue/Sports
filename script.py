import requests
from bs4 import BeautifulSoup
import pandas as pd

all_news = []

places = ["نادي", "مركز شباب", "ملعب", "حمام سباحة", "صالة"]
incidents = ["غرق", "حريق", "إصابة", "وفاة", "حادث", "اختناق"]

# ======================
# 🟢 YOUm7
# ======================
def scrape_youm7():
    base_url = "https://www.youm7.com/Section/حوادث/203/"
    results = []

    for page in range(1, 4):
        url = base_url + str(page)
        try:
            res = requests.get(url, timeout=20)
            soup = BeautifulSoup(res.content, "html.parser")

            for item in soup.find_all("h3"):
                a = item.find("a")
                if a:
                    title = a.text.strip()
                    link = "https://www.youm7.com" + a.get("href")

                    if any(p in title for p in places) and any(i in title for i in incidents):
                        results.append({"العنوان": title, "اللينك": link})
        except:
            continue

    return results

# ======================
# 🟢 CAIRO24
# ======================
def scrape_cairo24():
    url = "https://www.cairo24.com"
    results = []

    try:
        res = requests.get(url, timeout=20)
        soup = BeautifulSoup(res.content, "html.parser")

        for a in soup.find_all("a"):
            title = a.text.strip()
            link = a.get("href")

            if link and "cairo24" in link:
                if any(p in title for p in places) and any(i in title for i in incidents):
                    results.append({"العنوان": title, "اللينك": link})
    except:
        pass

    return results

# ======================
# 🟢 SHOROUK
# ======================
def scrape_shorouk():
    url = "https://www.shorouknews.com"
    results = []

    try:
        res = requests.get(url, timeout=20)
        soup = BeautifulSoup(res.content, "html.parser")

        for a in soup.find_all("a"):
            title = a.text.strip()
            link = a.get("href")

            if link and "shorouknews" in link:
                if any(p in title for p in places) and any(i in title for i in incidents):
                    results.append({"العنوان": title, "اللينك": link})
    except:
        pass

    return results

# ======================
# 🟢 ELWATAN
# ======================
def scrape_watan():
    url = "https://www.elwatannews.com"
    results = []

    try:
        res = requests.get(url, timeout=20)
        soup = BeautifulSoup(res.content, "html.parser")

        for a in soup.find_all("a"):
            title = a.text.strip()
            link = a.get("href")

            if link and "elwatannews" in link:
                if any(p in title for p in places) and any(i in title for i in incidents):
                    results.append({"العنوان": title, "اللينك": link})
    except:
        pass

    return results

# ======================
# 🚀 RUN ALL
# ======================

print("تشغيل اليوم السابع...")
all_news.extend(scrape_youm7())

print("تشغيل القاهرة 24...")
all_news.extend(scrape_cairo24())

print("تشغيل الشروق...")
all_news.extend(scrape_shorouk())

print("تشغيل الوطن...")
all_news.extend(scrape_watan())

# ======================
# 📊 SAVE
# ======================

df = pd.DataFrame(all_news)
df.drop_duplicates(inplace=True)

print("عدد الأخبار:", len(df))

df.to_excel("final_news.xlsx", index=False)

print("تم إنشاء الملف النهائي ✅")
