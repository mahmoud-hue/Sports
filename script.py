import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

base_url = "https://www.youm7.com/Section/حوادث/203/"
places = ["نادي", "مركز شباب", "صالة", "فرع نادي", "صالة رياضية"]

all_news = []

# نلف على أول 5 صفحات
for page in range(1, 6):
    print(f"Fetching page {page}...")
    url = base_url + str(page)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"خطأ في تحميل الصفحة {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    # في الصفحة الحقيقية العناوين بتكون داخل عناوين H3 تحت القسم
    # HTML يمكن يكون مختلف شوية، فحنجيب كل ال<a> اللي بتقف داخل الحوادث
    articles = soup.select("##main-container a")  # selector واسع

    for a_tag in articles:
        title = a_tag.get_text(strip=True)
        href = a_tag.get("href")

        # بعض النصوص ممكن ميبقاش عنوان خبر، نتأكد انه نص واضح
        if not title or len(title) < 5:
            continue

        # تاريخ بسيط هيتم تحليله بعدها
        date_text = ""  # ممكن نضيف لو نقدر نطلع التاريخ من DOM لاحقًا
        published = datetime.now().strftime("%d/%m/%Y")

        related = any(word in title for word in places)

        all_news.append({
            "التاريخ": published,
            "العنوان": title,
            "متعلق بنادي/مركز": related,
            "اللينك": href
        })

# تحويل ل DataFrame
df = pd.DataFrame(all_news).drop_duplicates(subset=["العنوان"])

print(f"عدد الأخبار المتجمعة: {len(df)}")

df.to_excel("youm7_incidents_clubs.xlsx", index=False)

print("تم إنشاء الملف بنجاح! ✅")
