from helium import start_firefox
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import os

def tmd():
    url = "https://www.tmd.go.th/climate/daily"
    browser = start_firefox(url, headless=True)
    time.sleep(5)

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

    # 🔍 พยายามอ่านจาก artifact ก่อน ถ้าไม่มี fallback ไป default
    artifact_path = os.path.join("artifact_data", "TMDdata.csv")
    default_path = "TMDdata.csv"
    file_path = artifact_path if os.path.exists(artifact_path) else default_path

    if os.path.exists(file_path):
        try:
            df_existing = pd.read_csv(file_path, encoding="utf-8-sig")
        except Exception as e:
            print("เกิดข้อผิดพลาดในการอ่านไฟล์:", e)
            df_existing = pd.DataFrame()
    else:
        df_existing = pd.DataFrame()

    # ตรวจสอบว่าข้อมูลของเมื่อวานมีอยู่แล้วหรือไม่
    is_duplicate = df_existing.merge(
        df_new[["สถานีอุตุนิยมวิทยา", "วันที่"]],
        on=["สถานีอุตุนิยมวิทยา", "วันที่"],
        how="inner"
    )

    if not is_duplicate.empty:
        print("ข้อมูลของเมื่อวานมีอยู่แล้ว ไม่ต้องบันทึกซ้ำ")
        return

    # รวมและลบข้อมูลซ้ำ
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset=["สถานีอุตุนิยมวิทยา", "วันที่"], keep="last", inplace=True)

    # บันทึกไฟล์ CSV ใหม่
    df_combined.to_csv("TMDdata.csv", index=False, encoding="utf-8-sig")
    print("บันทึกข้อมูลสำเร็จ:", "TMDdata.csv")

if __name__ == "__main__":
    tmd()
