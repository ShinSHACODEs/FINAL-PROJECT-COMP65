import pandas as pd
import os

url = "https://ourworldindata.org/grapher/temperature-anomaly.csv?v=1&csvType=full&useColumnShortNames=true"
file_path = "temperature_anomaly.csv"

# ดึงข้อมูลล่าสุดจาก URL
df_new = pd.read_csv(url)

# ถ้ามีไฟล์เดิมในโฟลเดอร์
if os.path.exists(file_path):
    df_old = pd.read_csv(file_path)

    # รวมข้อมูลเก่ากับข้อมูลใหม่
    df_combined = pd.concat([df_old, df_new], ignore_index=True)

    # ลบแถวที่ซ้ำกันทุกคอลัมน์
    df_combined = df_combined.drop_duplicates()

    # เซฟทับไฟล์เดิม
    df_combined.to_csv(file_path, index=False)
    print("✅ Updated CSV — appended only new rows & removed duplicates.")
else:
    # ถ้าไม่มีไฟล์เดิม ให้สร้างใหม่
    df_new.to_csv(file_path, index=False)
    print("✅ Saved new CSV file.")

print("Done ✅")
