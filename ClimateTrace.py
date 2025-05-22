import os
import pandas as pd
import requests
from datetime import datetime

file_id = "1RMmE2T8bV-oyFOUplkPaaslEc5htuox3"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, "climatecountry.csv", quiet=False)
df = pd.read_csv("climatecountry.csv")
print(df.head())

# ฟังก์ชันหาปีที่มากที่สุดจากไฟล์ CSV
def get_max_year(file_path):
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if 'Year' in df.columns and not df.empty:
                return df['Year'].max()
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
    return None

def urlCT3():
    current_year = datetime.now().year
    url = f"https://api.c10e.org/v6/country/emissions/timeseries/subsectors?since={current_year}&to={current_year}&download=csv&combined=false"
    response = requests.get(url)
    
    if response.status_code == 200:
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        temp_file = os.path.join(download_folder, "New_climatetrace.csv")
        with open(temp_file, 'wb') as f:
            f.write(response.content)

        # กำหนดไฟล์ปลายทาง
        target_folder = os.getcwd()
        target_file = os.path.join(target_folder, "climatecountry.csv") 

        # อ่านข้อมูลจากไฟล์ที่ดาวน์โหลด
        new_data = pd.read_csv(temp_file)

        # ตรวจสอบว่ามีข้อมูลใหม่หรือไม่
        if not new_data.empty:
            if os.path.exists(target_file):
                existing_data = pd.read_csv(target_file)
                combined_data = pd.concat([existing_data, new_data]).drop_duplicates()
                combined_data.to_csv(target_file, index=False)
                print(f"ข้อมูลถูกรวมและบันทึกที่: {target_file}")
        else:
            print("ไม่มีข้อมูลใหม่สำหรับการเพิ่ม")

        os.remove(temp_file)
    else:
        print(f"ดาวน์โหลดไม่สำเร็จ: รหัสสถานะ {response.status_code}")

urlCT3()
