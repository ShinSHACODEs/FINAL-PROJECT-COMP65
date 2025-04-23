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
    options.add_argument("--headless")  # ทำให้ไม่ต้องเปิดหน้าต่าง Chrome
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://www.tmd.go.th/climate/daily"
    driver.get(url)

    time.sleep(30)
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[5]/div/div[3]/div/div/div/table')))
        climate_data = driver.find_elements(By.XPATH, '/html/body/main/div/div[5]/div/div[3]/div/div/div/table/tbody/tr')
        
        # ดึงข้อมูลเมื่อวาน
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # สร้างรายการเพื่อเก็บข้อมูลจากแต่ละแถว
        rows = []
        for data in climate_data:
            columns = data.find_elements(By.TAG_NAME, "td")
            row = [col.text.strip() for col in columns]  # ใช้ .strip() เพื่อลบช่องว่างที่ไม่จำเป็น
            if row:  # ตรวจสอบว่า row ไม่ใช่ค่าว่าง
                rows.append(row + [yesterday])  # เพิ่มคอลัมน์วันที่

        # สร้าง DataFrame จากข้อมูลที่ดึงมา
        df_new = pd.DataFrame(rows, columns=["สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
                                             "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี", "วันที่"])
        file_path = "TMDdata.csv"

        if os.path.exists(file_path):
            df_existing = pd.read_csv(file_path, encoding="utf-8-sig")

            # ตรวจสอบว่าข้อมูลของสถานีและวันที่ซ้ำแล้วหรือไม่ (ข้ามเวลาที่เปลี่ยนแปลง)
            if any((df_existing["วันที่"] == yesterday) & (df_existing["สถานีอุตุนิยมวิทยา"].isin(df_new["สถานีอุตุนิยมวิทยา"]))):
                print("ข้อมูลของเมื่อวานมีอยู่แล้ว ไม่ต้องบันทึก")
                driver.quit()
                return

            # รวมข้อมูลใหม่กับข้อมูลเดิม
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)

            # ลบข้อมูลซ้ำโดยใช้ "สถานีอุตุนิยมวิทยา" และ "วันที่" เป็น key
            df_combined = df_combined.drop_duplicates(subset=["สถานีอุตุนิยมวิทยา", "วันที่"], keep="last")
        else:
            df_combined = df_new

        # บันทึกข้อมูลลง CSV
        df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
        print("บันทึกข้อมูลสำเร็จ:", file_path)

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

    finally:
        driver.quit()
# เรียกใช้งานฟังก์ชัน
tmd()
