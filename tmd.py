from datetime import datetime, timedelta
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def tmd():
    options = Options()
    options.add_argument("--headless=new")  # ใช้ headless แบบใหม่
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    url = "https://www.tmd.go.th/climate/daily"
    driver.get(url)

    try:
        # รอให้โหลดตาราง
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//table[contains(@class, "table")]')))
        time.sleep(5)  # เผื่อโหลดช้า เพิ่ม buffer

        climate_data = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        rows = []

        for data in climate_data:
            columns = data.find_elements(By.TAG_NAME, "td")
            row = [col.text.strip() for col in columns]
            if len(row) == 8:
                row.append(yesterday)
                rows.append(row)
        if not rows:
            print("ไม่มีรายงานสภาพอากาศสำหรับเมื่อวาน")
            return

        df_new = pd.DataFrame(rows, columns=[
            "สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
            "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี", "วันที่"
        ])

        file_path = "TMDdata.csv"
        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path, encoding="utf-8-sig")
            if any((df_existing["วันที่"] == yesterday) & (df_existing["สถานีอุตุนิยมวิทยา"].isin(df_new["สถานีอุตุนิยมวิทยา"]))):
                print("ข้อมูลของเมื่อวานมีอยู่แล้ว ไม่ต้องบันทึก")
                driver.quit()
                return
            df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(
                subset=["สถานีอุตุนิยมวิทยา", "วันที่"], keep="last")
        else:
            df_combined = df_new

        df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
        print("บันทึกข้อมูลสำเร็จ:", file_path)
        
    finally:
        driver.quit()

tmd()
