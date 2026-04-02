import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.youm7.com/Section/حوادث/203/1"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

news_list = []

# الأخبار في اليوم السابع بتكون غالبًا في h3 جوا div فيه class فيه "title"
for item in soup.find_all("h3"):
    a_tag = item.find("a")
    
    if a_tag and a_tag.get("href"):
        title = a_tag.text.strip()
        link = "https://www.youm7.com" + a_tag.get("href")

        news_list.append({
            "العنوان": title,
            "اللينك": link
        })

df = pd.DataFrame(news_list)

print("عدد الأخبار:", len(df))
print(df.head(10))

df.to_excel("youm7_test.xlsx", index=False)

print("تم إنشاء الملف ✅")
