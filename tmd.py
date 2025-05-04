from helium import start_firefox
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import gdown

file_id = "1O2HqNcX77-uGv8BL05AmFtxxFqqe0qPE"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, "TMDdata.csv", quiet=False)
df = pd.read_csv("TMDdata.csv")
print(df.head())

def tmd():
    url = "https://www.tmd.go.th/climate/daily"
    browser = start_firefox(url, headless=True)
    
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    tables = soup.find_all('table', class_='table')
    
    rows = []
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    #ส่วนดึงข้างใน table
    for table in tables:
        rows_in_table = table.find_all('tr')
        for row in rows_in_table:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells] # ดึง text ออกมา cell
            if row_data and row_data[0] != 'กำลังโหลดข้อมูล...':
                row_data.append(yesterday)
                rows.append(row_data)
    browser.quit()
    
    columns = [
        "สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
        "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี", "วันที่"
    ]
    df_new = pd.DataFrame(rows, columns=columns)
    if len(df_new) > 0:
        df_new = df_new.drop(index=[])
     
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
