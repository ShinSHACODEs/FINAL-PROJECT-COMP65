import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def weather():
    url = "https://www.timeanddate.com/weather/?low=4&sort=1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

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
    df_new['Timestamp'] = datetime.now().strftime('%Y-%m-%d')  # เพิ่มคอลัมน์ timestamp

    file_path = "weatherdata.csv"

    if os.path.exists(file_path):
        # อ่านข้อมูลเดิมจากไฟล์ CSV
        df_existing = pd.read_csv(file_path, encoding="utf-8-sig")

        # เปรียบเทียบแค่ข้อมูลในคอลัมน์ที่สำคัญ เช่น "Country-City" และ "Date" หากข้อมูลใหม่ต่างจากเดิม
        new_data_check = df_new[['Country-City', 'Date']].values
        existing_data_check = df_existing[['Country-City', 'Date']].values

        # ตรวจสอบว่ามีข้อมูลใหม่ที่ไม่ซ้ำหรือไม่
        if (new_data_check == existing_data_check).all():
            print("ข้อมูลไม่เปลี่ยนแปลง ไม่ต้องบันทึกใหม่")
            return

        # ถ้ามีการเปลี่ยนแปลงให้ append ข้อมูลใหม่
        df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(subset=["Country-City", "Date"])
    else:
        df_combined = df_new

    # บันทึกข้อมูลลงไฟล์ CSV
    df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
    print("ข้อมูลอัพเดทสำเร็จ:")
    print(df_combined)

weather()
