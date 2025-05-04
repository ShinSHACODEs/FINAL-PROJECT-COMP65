from helium import start_firefox
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import gdown

def tmd():
    url = "https://www.tmd.go.th/climate/daily"
    browser = start_firefox(url, headless=True)
    
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    tables = soup.find_all('table', class_='table')
    
    rows = []
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # ดึงข้อมูลจากแต่ละ table
    for table in tables:
        rows_in_table = table.find_all('tr')
        for row in rows_in_table:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data and row_data[0] != 'กำลังโหลดข้อมูล...' and len(row_data) == 8:
                rows.append(row_data)
    browser.quit()
    
    columns = [
        "สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
        "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี"
    ]
    
    df_new = pd.DataFrame(rows, columns=columns)
    
    # เพิ่มคอลัมน์ 'วันที่' ทีหลัง
    df_new["วันที่"] = yesterday

    # ถ้าจำเป็นต้องลบแถวบางแถว (กำหนด index ตามต้องการ)
    if len(df_new) > 0:
        df_new = df_new.drop(index=[])  # ยังไม่ลบแถวใด
    
    file_path = "TMDdata.csv"
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path, encoding="utf-8-sig")
        
        if any((df_existing["วันที่"] == yesterday) & (df_existing["สถานีอุตุนิยมวิทยา"].isin(df_new["สถานีอุตุนิยมวิทยา"]))):
            print("ข้อมูลของเมื่อวานมีอยู่แล้ว ไม่ต้องบันทึก")
            return
        
        df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(
            subset=["สถานีอุตุนิยมวิทยา", "วันที่"], keep="last")
    else:
        df_combined = df_new
    
    df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
    print("บันทึกข้อมูลสำเร็จ:", file_path)

tmd()

