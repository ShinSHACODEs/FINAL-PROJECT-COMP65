from helium import start_firefox
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import gdown
import os

def tmd():
    url = "https://www.tmd.go.th/climate/daily"
    browser = start_firefox(url, headless=True)
    time.sleep(5)  # รอให้โหลดเสร็จ
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()

    tables = soup.find_all('table', class_='table')
    rows = []
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    for table in tables:
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data and row_data[0] != 'กำลังโหลดข้อมูล...':
                # ตรวจสอบว่ามีกี่ช่อง
                if len(row_data) < 8:
                    row_data += [None] * (8 - len(row_data))
                elif len(row_data) > 8:
                    row_data = row_data[:8]
                rows.append(row_data)
            
    columns = [
        "สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
        "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี"
    ]

    df_new = pd.DataFrame(rows, columns=columns)
    df_new["วันที่"] = yesterday
    print(df_new)
    
    file_id = "16YaoLa0RNTqnQQ-kcyg2jA8Q2OCVneSq"
    url2 = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url2, "TMDdata.csv", quiet=False)
    df_old = "TMDdata.csv"
    
     if os.path.exists("TMDdata.csv"):
        try:
            df_old = pd.read_csv("TMDdata.csv", encoding="utf-8-sig")
        except Exception as e:
            print(f"ไม่สามารถอ่านไฟล์ได้: {e}")
            return

        # ตรวจสอบข้อมูลซ้ำ
        is_duplicate = df_old.merge(
            df_new[["สถานีอุตุนิยมวิทยา", "วันที่"]],
            on=["สถานีอุตุนิยมวิทยา", "วันที่"],
            how="inner"
        )
        if not is_duplicate.empty:
            print("ข้อมูลของเมื่อวานมีอยู่แล้ว ไม่ต้องบันทึก")
            return
    else:
        # ถ้าไม่มี df_old ให้ตั้งค่าเป็น DataFrame ว่าง
        df_old = pd.DataFrame()

    # รวมข้อมูลและลบข้อมูลที่ซ้ำ
    df_combined = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates(
        subset=["สถานีอุตุนิยมวิทยา", "วันที่"], keep="last"
    )

    # บันทึกข้อมูลใหม่ลงในไฟล์
    df_combined.to_csv("TMDdata.csv", index=False, encoding="utf-8-sig")
    print("บันทึกข้อมูลสำเร็จ")

tmd()
