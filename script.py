import requests
from bs4 import BeautifulSoup
import pandas as pd

all_news = []

places = ["نادي", "مركز شباب", "ملعب", "حمام سباحة"]
incidents = ["غرق", "حريق", "إصابة", "وفاة", "حادث"]

# ======================
# 🟢 YOUm7 (مظبوط)
# ======================
def scrape_youm7():
    results = []
    for page in range(1, 6):
        url = f"https://www.youm7.com/Section/حوادث/203/{page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")

        for h in soup.find_all("h3"):
            a = h.find("a")
            if a:
                title = a.text.strip()
                link = "https://www.youm7.com" + a["href"]

                if any(p in title for p in places) and any(i in title for i in incidents):
                    results.append({"العنوان": title, "اللينك": link})

    return results

# ======================
# 🟢 CAIRO24 (قسم حوادث)
# ======================
def scrape_cairo24():
    url = "https://www.cairo24.com/section/33"
    results = []

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    for h in soup.find_all("h3"):
        a = h.find("a")
        if a:
            title = a.text.strip()
            link = a["href"]

            if any(p in title for p in places) and any(i in title for i in incidents):
                results.append({"العنوان": title, "اللينك": link})

    return results

# ======================
# 🟢 ELWATAN (قسم حوادث)
# ======================
def scrape_watan():
    url = "https://www.elwatannews.com/section/115"
    results = []

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    for h in soup.find_all("h2"):
        a = h.find("a")
        if a:
            title = a.text.strip()
            link = a["href"]

            if any(p in title for p in places) and any(i in title for i in incidents):
                results.append({"العنوان": title, "اللينك": link})

    return results

# ======================
# 🚀 تشغيل
# ======================
print("youm7...")
all_news.extend(scrape_youm7())

print("cairo24...")
all_news.extend(scrape_cairo24())

print("watan...")
all_news.extend(scrape_watan())

# ======================
# 📊 حفظ
# ======================
df = pd.DataFrame(all_news)
df.drop_duplicates(inplace=True)

print("عدد الأخبار:", len(df))

df.to_excel("final_news.xlsx", index=False)

print("تم ✅")
