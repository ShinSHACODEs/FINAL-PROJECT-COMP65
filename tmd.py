from helium import start_firefox
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
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
            if row_data and row_data[0] != 'กำลังโหลดข้อมูล...' and len(row_data) == 8:
                rows.append(row_data)

    columns = [
        "สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
        "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี"
    ]

    df_new = pd.DataFrame(rows, columns=columns)
    df_new["วันที่"] = yesterday

    file_path = "TMDdata.csv"
    if os.path.exists(file_path):
        try:
            df_existing = pd.read_csv(file_path, encoding="utf-8-sig")
        except Exception as e:
            print("เกิดข้อผิดพลาดในการอ่านไฟล์:", e)
            df_existing = pd.DataFrame()

        # เช็คว่ามีข้อมูลของวันนั้นแล้วหรือยัง
        is_duplicate = df_existing.merge(
            df_new[["สถานีอุตุนิยมวิทยา", "วันที่"]],
            on=["สถานีอุตุนิยมวิทยา", "วันที่"],
            how="inner"
        )

        if not is_duplicate.empty:
            print("ข้อมูลของเมื่อวานมีอยู่แล้ว ไม่ต้องบันทึก")
            return

        # รวมและลบซ้ำ
        df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(
            subset=["สถานีอุตุนิยมวิทยา", "วันที่"], keep="last"
        )
    else:
        df_combined = df_new

    # บันทึก
    df_combined.to_csv(file_path, index=False, encoding="utf-8-sig")
    print("บันทึกข้อมูลสำเร็จ:", file_path)

if __name__ == "__main__":
    tmd()
