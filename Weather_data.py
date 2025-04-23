import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def weather():
    url = "https://www.timeanddate.com/weather/?low=4&sort=1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # ดึงข้อมูลจากการ soup
    primary = soup.find('div', class_="tb-scroll")
    data = []
    for row in primary.findAll('tr'):
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]
        if row_data:
            data.append(row_data)

    # สร้าง DataFrame จากข้อมูลที่ดึงมา
    df_new = pd.DataFrame(data, columns=["Country-City", "Date", "img", "Temperature"])
    df_new.drop(["img"], axis=1, inplace=True)  # ลบคอลัมน์ img
    today = datetime.now().strftime('%Y-%m-%d')
    df_new['Timestamp'] = today  # ใช้ฟอร์แมตเดียวตลอด

    file_path = "weatherdata.csv"

    # ถ้ามีไฟล์อยู่แล้ว ให้ต่อข้อมูลใหม่เข้าไปเลย ไม่ต้องเช็คซ้ำ
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path, encoding="utf-8-sig")
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
        print("ข้อมูลถูกรวมและบันทึกลงไฟล์แล้ว:")
        print(df_combined)

weather()
