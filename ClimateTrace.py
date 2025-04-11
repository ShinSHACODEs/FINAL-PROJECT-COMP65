import requests
from datetime import datetime
import os
import pandas as pd
import time
import glob
from selenium import webdriver

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
    
    # ตั้งค่า Chrome WebDriver
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    option.add_experimental_option("prefs", {"download.default_directory": download_folder})
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    
    # รอให้ดาวน์โหลดเสร็จ
    time.sleep(10)  
    driver.quit()

    # ค้นหาไฟล์ที่ดาวน์โหลด
    trace_files = glob.glob(os.path.join(download_folder, "trace*.csv"))
    if not trace_files:
        print("ไม่พบไฟล์ที่ดาวน์โหลด")
        return
    
    # ใช้ไฟล์ที่เจอล่าสุด
    downloaded_file = max(trace_files, key=os.path.getctime)
    renamed_file = os.path.join(download_folder, "climatetrace_country.csv")
    os.rename(downloaded_file, renamed_file)
    
    # กำหนดไฟล์ปลายทาง
    target_folder = os.getcwd()
    target_file = os.path.join(target_folder, "climatecountry.csv") 
    
    # อ่านข้อมูลใหม่จากไฟล์ที่เปลี่ยนชื่อ
    new_data = pd.read_csv(renamed_file)
    
    # ตรวจสอบว่ามีข้อมูลใหม่หรือไม่
    if not new_data.empty:
        if os.path.exists(target_file):
            existing_data = pd.read_csv(target_file)
            combined_data = pd.concat([existing_data, new_data]).drop_duplicates()
            combined_data.to_csv(target_file, index=False)
        else:
            new_data.to_csv(target_file, index=False)
        
        print(f"ข้อมูลถูกรวมและบันทึกที่: {target_file}")
    else:
        print("ไม่มีข้อมูลใหม่สำหรับการเพิ่ม")
    
    # ลบไฟล์ที่เปลี่ยนชื่อแล้ว
    os.remove(renamed_file)
    print(f"ไฟล์ที่เปลี่ยนชื่อถูกลบ: {renamed_file}")
urlCT3()
