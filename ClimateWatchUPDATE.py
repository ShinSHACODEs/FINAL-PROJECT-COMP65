import pandas as pd
from datetime import datetime
import requests
import sys
import ast
import os
import gdown

# อ่านไฟล์เก่า
file_id = "15j66Oa58FrQ-ad_CJtT5BGd-s6NBhxg8"
url2 = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url2, "ClimateWatchDATA.csv", quiet=False)
df_old = "ClimateWatchDATA.csv"

# ฟังก์ชันตรวจสอบปีล่าสุดในไฟล์
def max_year(filename="ClimateWatchDATA.csv"):
    try:
        df = pd.read_csv(filename)

        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')  # แปลงเป็นตัวเลข
            return int(df['year'].max())
        else:
            print("คอลัมน์ 'year' ไม่พบในไฟล์")
            return None
    except FileNotFoundError:
        print(f"ไม่พบไฟล์ {filename}")
        return None
    
# ฟังก์ชันดึงข้อมูลจาก ClimateWatch API
def urlCW(source_id, gas_id, max_pages=200):
    start_year = max_year()
    end_year = datetime.now().year

    if start_year >= end_year:
        print(f"มีข้อมูลปีล่าสุด ({start_year}) อยู่แล้ว ไม่ต้องดึงข้อมูลใหม่.")
        sys.exit()

    base_URL = "https://www.climatewatchdata.org/api/v1/data/historical_emissions?source_ids[]=226&gas_ids[]=489&page=1&per_page=200&sector_ids[]=2641&sector_ids[]=2641&sort_col=2022&sort_dir=DESC"
    all_data = []
    page = 1

    while True:
        params = {
            "source_ids[]": source_id,
            "gas_ids[]": gas_id,
            "page": page,
            "per_page": 10000,
            "start_year": start_year,
            "end_year": end_year,
            "sort_col": "country",
            "sort_dir": "ASC"
        }
        response = requests.get(base_URL, params=params)
        data = response.json()

        if not data.get("data"):
            break

        all_data.extend(data["data"])

        if page < max_pages:
            page += 1
        else:
            break

    df = pd.DataFrame(all_data).dropna().reset_index(drop=True)
    df.to_csv("ClimateWatchUPDATE.csv", index=False)
    print("บันทึกข้อมูลเรียบร้อย: ClimateWatchUPDATE.csv")

# เรียกใช้ฟังก์ชันดึงข้อมูลจาก API
source_id = [214]
gas_id = [490, 491, 492, 493]
urlCW(source_id, gas_id)
    
def fixyear():
# อ่านไฟล์ CSV
    original_file = pd.read_csv('ClimateWatchData.csv')
    climatewatch_update = pd.read_csv('ClimateWatchUPDATE.csv')
    
    # แปลงให้เป็นลิสต์ถ้ามีการใช้ string รูปแบบ list โดยใช้ ast.literal_eval()
    climatewatch_update['emissions'] = climatewatch_update['emissions'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # ใช้ explode เพื่อแยกข้อมูลจาก 'emissions' ออกเป็นหลายแถว
    climatewatch_update_exploded = climatewatch_update.explode('emissions').reset_index(drop=True)

    # แยกคอลัมน์ 'year' และ 'value' จาก 'emissions'
    climatewatch_update_exploded[['year', 'value']] = pd.DataFrame(climatewatch_update_exploded['emissions'].tolist(), index=climatewatch_update_exploded.index)

    # ลบคอลัมน์ 'emissions'
    climatewatch_update_exploded.drop(columns=['emissions'], inplace=True)

    # รวมข้อมูลจากทั้งสอง DataFrame เก่า
    combined_data = pd.concat([climatewatch_update_exploded, original_file], ignore_index=True)

    # ลบแถวที่ซ้ำกัน
    combined_data.drop_duplicates(inplace=True)

    # บันทึกผลลัพธ์ลงในไฟล์ CSV
    combined_data.to_csv('ClimateWatchDATA.csv', index=False)
    print("\nข้อมูลถูกรวมและบันทึกลงในไฟล์ 'ClimateWatchDATA_Transformed_Updated.csv' แล้ว.")
    
    os.remove("ClimateWatchUPDATE.csv")
fixyear()
