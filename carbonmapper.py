import requests
import pandas as pd
from datetime import datetime
import io
import shutil
import os

def comapper():
    url = "https://api.carbonmapper.org/api/v1/catalog/plume-csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            # แปลง response content เป็น DataFrame
            read_file = pd.read_csv(io.StringIO(response.text))
            
            # เพิ่มคอลัมน์ Timestamp
            read_file['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # บันทึกข้อมูลลงไฟล์ CSV
            file_name = "plume_data.csv"
            read_file.to_csv(file_name, index=False)
            print("บันทึกข้อมูลเรียบร้อย")
            
            # ดึงที่อยู่ของโฟลเดอร์ที่โค้ดทำงาน
            target_folder = os.path.dirname(os.path.realpath(__file__))
            
            # สร้าง path ของไฟล์ในโฟลเดอร์เดียวกับโค้ด
            target_file = os.path.join(target_folder, file_name)
            
            # ย้ายไฟล์ที่ดาวน์โหลดไปยังโฟลเดอร์เดียวกับไฟล์โค้ด
            shutil.move(file_name, target_file)
            print(f"ย้ายไฟล์ไปยัง: {target_file}")
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการประมวลผล CSV: {e}")

comapper()
