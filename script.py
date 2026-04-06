import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "5e999ed60e344940a89b94fd4a8291b3"

query = "حادث نادي OR حريق نادي OR غرق نادي OR حادث مركز شباب OR إصابة ملعب"

start_date = datetime(2026, 3, 1)
end_date = datetime(2026, 3, 31)

all_news = []

exclude_words = ["تعزية", "نعي", "تكريم", "وفاة لاعب", "يهنئ", "احتفال"]

current_date = start_date

while current_date <= end_date:
    next_date = current_date + timedelta(days=1)

    from_date = current_date.strftime("%Y-%m-%d")
    to_date = next_date.strftime("%Y-%m-%d")

    print(f"جاري جلب أخبار يوم: {from_date}")

    url = f"https://newsapi.org/v2/everything?q={query}&language=ar&from={from_date}&to={to_date}&sortBy=publishedAt&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])

    for article in articles:
        title = article["title"]
        link = article["url"]
        date = article["publishedAt"]

        if not any(word in title for word in exclude_words):
            all_news.append({
                "التاريخ": date,
                "العنوان": title,
                "اللينك": link
            })

    current_date = next_date

# ==========================
# تحويل ل DataFrame
df = pd.DataFrame(all_news)

# إزالة التكرار
df.drop_duplicates(inplace=True)

print("إجمالي الأخبار:", len(df))

# حفظ
df.to_excel("march_full_news.xlsx", index=False)

print("تم إنشاء الملف الكامل لشهر مارس ✅")
