import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver

def urlCarMo():
    # ตั้งค่า Chrome WebDriver
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)

    # กำหนดโฟลเดอร์ดาวน์โหลด
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    option.add_experimental_option("prefs", {"download.default_directory": download_folder})

    driver = webdriver.Chrome(options=option)
    driver.get("https://datas.carbonmonitor.org/API/downloadFullDataset.php?source=carbon_global")

    # รอให้การดาวน์โหลดเสร็จสมบูรณ์
    time.sleep(15)
    driver.quit()

    # ตรวจสอบไฟล์ล่าสุดในโฟลเดอร์ดาวน์โหลด
    downloaded_files = [f for f in os.listdir(download_folder) if f.startswith("carbonmonitor")]
    if not downloaded_files:
        print("ไม่พบไฟล์ที่ดาวน์โหลด!")
        return

    # หาชื่อไฟล์ล่าสุด
    downloaded_files.sort(key=lambda x: os.path.getctime(os.path.join(download_folder, x)), reverse=True)
    latest_file = downloaded_files[0]

    # ย้ายไฟล์ไปยังโฟลเดอร์ที่โค้ดทำงานอยู่
    target_folder = os.getcwd()
    source_path = os.path.join(download_folder, latest_file)

    # กำหนดชื่อไฟล์ปลายทาง
    combined_path = os.path.join(target_folder, "carbon_monitor.csv")

    # อ่านข้อมูลใหม่จากไฟล์ที่ดาวน์โหลด (ลบคอลัมน์ที่ไม่มีชื่อออก)
    new_data = pd.read_csv(source_path).drop(columns=[col for col in pd.read_csv(source_path).columns if "Unnamed" in col], errors='ignore')

    # เพิ่ม Timestamp ให้ข้อมูลใหม่
    new_data['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # บันทึกข้อมูลใหม่โดยการเขียนทับไฟล์ปลายทาง
    new_data.to_csv(combined_path, index=False)
    print(f"ข้อมูลถูกเขียนทับและบันทึกที่: {combined_path}")

    # ลบไฟล์ที่ดาวน์โหลด
    os.remove(source_path)
    print(f"ไฟล์ที่ดาวน์โหลดถูกลบ: {source_path}")

urlCarMo()
