import os
import pandas as pd
import requests
import gdown

file_id = "161FmRz3oR8kGsSwVnHFLyO5JmCDlvXl6"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, "carbon_monitor.csv", quiet=False)
df = pd.read_csv("carbon_monitor.csv")
print(df.head())

def download_carbon_monitor_csv():
    url = "https://datas.carbonmonitor.org/API/downloadFullDataset.php?source=carbon_global"
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(download_folder, exist_ok=True)
    
    filename = os.path.join(download_folder, "carbonmonitor_download.csv")

    # ดาวน์โหลดไฟล์
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"ดาวน์โหลดสำเร็จ: {filename}")
    else:
        print(f"ดาวน์โหลดล้มเหลว: รหัส {response.status_code}")
        return

    # อ่านไฟล์ที่โหลดมาใหม่
    df_new = pd.read_csv(filename)

    # ลบคอลัมน์ที่ไม่ต้องการ เช่น Unnamed
    df_new = df_new.drop(columns=lambda c: c.startswith("Unnamed"), errors='ignore')

    dest = os.path.join(os.getcwd(), "carbon_monitor.csv")

    # รวมข้อมูลใหม่กับเก่า ถ้ามีไฟล์เดิมอยู่แล้ว
    if os.path.exists(dest):
        df_old = pd.read_csv(dest)
        df_combined = pd.concat([df_old, df_new]).drop_duplicates(ignore_index=True)

        if df_combined.shape[0] == df_old.shape[0]:
            print("ข้อมูลไม่เปลี่ยนแปลง!")
            os.remove(filename)
            return
    else:
        df_combined = df_new

    # บันทึกข้อมูล
    df_combined.to_csv(dest, index=False)
    print(f"ข้อมูลบันทึกที่: {dest}")
    os.remove(filename)
    print(f"ลบไฟล์ดาวน์โหลดแล้ว: {filename}")

download_carbon_monitor_csv()

