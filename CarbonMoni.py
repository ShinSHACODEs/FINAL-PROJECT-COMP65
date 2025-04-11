import os, time, pandas as pd
from selenium import webdriver

def urlCarMo():
    # ตั้งค่า WebDriver
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": download_folder})
    driver = webdriver.Chrome(options=options)
    driver.get("https://datas.carbonmonitor.org/API/downloadFullDataset.php?source=carbon_global")
    time.sleep(15)
    driver.quit()

    # หาไฟล์ล่าสุด
    files = [f for f in os.listdir(download_folder) if f.startswith("carbonmonitor")]
    if not files:
        print("ไม่พบไฟล์ที่ดาวน์โหลด!")
        return
    files.sort(key=lambda f: os.path.getctime(os.path.join(download_folder, f)), reverse=True)
    latest = os.path.join(download_folder, files[0])

    # โหลดและลบคอลัมน์ Unnamed
    df_new = pd.read_csv(latest).drop(columns=lambda c: c.startswith("Unnamed"), errors='ignore')
    dest = os.path.join(os.getcwd(), "carbon_monitor.csv")

    if os.path.exists(dest):
        df_old = pd.read_csv(dest)

        # ตรวจสอบว่าไฟล์ใหม่และเก่ามีข้อมูลเหมือนกันหรือไม่
        # หากข้อมูลไม่ซ้ำกัน จะรวมข้อมูลใหม่ที่ไม่มีในไฟล์เก่า
        df_combined = pd.concat([df_old, df_new]).drop_duplicates(ignore_index=True)

        # ถ้าไม่มีการเปลี่ยนแปลงในข้อมูล
        if df_combined.shape[0] == df_old.shape[0]:
            print("ข้อมูลไม่เปลี่ยนแปลง!")
            os.remove(latest)  # ลบไฟล์ใหม่
            return
    else:
        df_combined = df_new

    # บันทึกข้อมูลที่รวมลงในไฟล์
    df_combined.to_csv(dest, index=False)
    print(f"ข้อมูลบันทึกที่: {dest}")
    os.remove(latest)
    print(f"ลบไฟล์ดาวน์โหลดแล้ว: {latest}")

urlCarMo()
