import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# إعدادات
base_url = "https://www.youm7.com/Section/حوادث/203/"
all_news = []
places = ["نادي", "مركز شباب"]
timeout_seconds = 30
max_retries = 3
pages_to_scrape = 5

for page in range(1, pages_to_scrape + 1):
    print(f"جاري فتح الصفحة {page}...")

    url = base_url + str(page)

    # Retry mechanism
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout_seconds)
            break
        except requests.exceptions.ReadTimeout:
            print(f"Timeout! محاولة {attempt + 1} من {max_retries}")
            time.sleep(5)  # استنى 5 ثواني قبل محاولة تانية
    else:
        print(f"فشل بعد {max_retries} محاولات للصفحة {page}")
        continue  # نعدي للصفحة التالية

    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("h3")

    if not items:
        print(f"لا أخبار في الصفحة {page}")
        continue

    for item in items:
        a_tag = item.find("a")
        if a_tag and a_tag.get("href"):
            title = a_tag.text.strip()
            link = "https://www.youm7.com" + a_tag.get("href")

            # تصفية الأخبار حسب النوادي / مراكز الشباب
            if any(word in title for word in places):
                all_news.append({
                    "التاريخ": datetime.now().strftime("%d/%m/%Y"),
                    "العنوان": title,
                    "اللينك": link
                })

# تحويل للـ DataFrame وحفظ Excel
df = pd.DataFrame(all_news)
print(f"عدد الأخبار بعد التصفية: {len(df)}")
df.to_excel("youm7_filtered_smart.xlsx", index=False)
print("تم إنشاء الملف ✅")
