import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def weather():
    url = "https://www.timeanddate.com/weather/?low=4&sort=1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    #ดึงข้อมูลจากการ soup
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
    df_new['Timestamp'] = datetime.now().strftime('%Y-%m-%d')  # เพิ่มคอลัมน์ timestamp ให้ข้อมูลใหม่

    file_path = "weatherdata.csv"

    if os.path.exists(file_path):
        # อ่านข้อมูลเดิมจากไฟล์ CSV
        df_existing = pd.read_csv(file_path, encoding="utf-8-sig")

        # ตรวจสอบข้อมูลใหม่ที่ยังไม่มีใน df_existing
        new_data_check = df_new[["Country-City", "Date", "Temperature"]]
        existing_data_check = df_existing[['Country-City', 'Date', "Temperature"]]

        # หา rows ที่ยังไม่มีใน df_existing
        new_rows = new_data_check[~new_data_check.apply(tuple, 1).isin(existing_data_check.apply(tuple, 1))]

        if not new_rows.empty:
            # ถ้ามีข้อมูลใหม่ให้เพิ่ม Timestamp
            new_rows['Timestamp'] = datetime.now().strftime('%Y-%m-%d')
            
            # รวมข้อมูลเดิมกับข้อมูลใหม่
            df_combined = pd.concat([df_existing, new_rows], ignore_index=True).drop_duplicates(subset=["Country-City", "Date","Temperature"])
            
            # บันทึกข้อมูลลงไฟล์ CSV
            df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
            print("ข้อมูลอัพเดทสำเร็จ:")
            print(df_combined)
        else:
            print("ข้อมูลไม่เปลี่ยนแปลง ไม่ต้องบันทึกใหม่")
    else:
        # ถ้าไฟล์ CSV ยังไม่มีให้สร้างใหม่
        df_new.to_csv(file_path, index=False, encoding="utf-8-sig")
        print("ข้อมูลถูกบันทึกครั้งแรก:")
        print(df_new)

weather()
