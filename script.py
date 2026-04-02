import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# الكلمات المفتاحية لتحديد الأخبار المتعلقة بالنوادي/مراكز الشباب
places = ["نادي", "مركز شباب", "صالة رياضية"]

# تاريخ البداية
start_date = datetime(2026, 3, 1)

# صفحة الحوادث اليوم السابع
base_url = "https://www.youm7.com/Section/حوادث"

# القائمة النهائية للأخبار
all_news = []

# صفحات نبدأ بيها (مثلاً أول 5 صفحات للتجربة)
num_pages = 8

for page in range(1, num_pages + 1):
    url = f"{base_url}?page={page}"
    print(f"جاري فتح الصفحة {page}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"فشل فتح الصفحة {page}، status code: {response.status_code}")
            continue
    except Exception as e:
        print(f"حدث خطأ في الصفحة {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    
    # كل خبر في الصفحة
    articles = soup.find_all("div", class_="newsTitle")  # تأكد من class حسب HTML الفعلي
    
    for art in articles:
        title_tag = art.find("a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href")
        
        # بعض الأخبار ممكن تحتوي على span للتاريخ أو div آخر حسب الصفحة
        # نجرب ناخد التاريخ من اليوم الحالي كبديل إذا مش موجود
        published = datetime.now()
        
        # فلترة حسب التاريخ
        if published >= start_date:
            related = any(word in title for word in places)
            all_news.append({
                "التاريخ": published.strftime("%d/%m/%Y"),
                "العنوان": title,
                "متعلق بنادي/مركز": related,
                "اللينك": link
            })

# تحويل ل DataFrame وحفظ Excel
df = pd.DataFrame(all_news)
print(f"عدد الأخبار بعد التصفية: {len(df)}")
df.to_excel("youm7_incidents_clubs.xlsx", index=False)
print("تم إنشاء الملف ✅")
