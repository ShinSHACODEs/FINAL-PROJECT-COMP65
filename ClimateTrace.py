import requests
from datetime import datetime
import os
import pandas as pd
import time
from selenium import webdriver

# ฟังก์ชันหาปีที่มากที่สุดจากไฟล์ CSV
def get_max_year(file_path):
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if 'Year' in df.columns and not df.empty:
                return df['Year'].max()
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
    return None

# ดึงข้อมูลจาก API
def urlCT():
    gases = ["co2e_100yr", "co2", "n2o", "ch4"]
    current_year = datetime.now().year
    start_year = get_max_year("ClimateTraceArea.csv")  # อ่านปีล่าสุดจากไฟล์ CSV

    # หากปีล่าสุดที่มีข้อมูลคือปีปัจจุบันหรือมากกว่า
    if start_year and start_year >= current_year:
        print(f"ข้อมูลสำหรับปี {current_year} ได้รับการอัพเดทแล้ว")
        return

    print(f"กำลังดึงข้อมูลสำหรับปี {current_year}...")

    results = []

    # ดึงข้อมูลจาก API สำหรับแต่ละแก๊ส
    for gas in gases:
        url = f"https://api.c10e.org/v6/app/assets?year={current_year}&gas={gas}&subsectors="
        try:
            response = requests.get(url, timeout=30)  # เพิ่ม timeout
            response.raise_for_status()  # ตรวจสอบข้อผิดพลาด HTTP

            json_data = response.json()

            if "assets" in json_data and json_data["assets"]:
                df = pd.DataFrame(json_data["assets"])
                df["year"] = current_year
                df["gas"] = gas
                results.append(df)
                print(f"Fetched: Gas={gas}, Year={current_year}")
            else:
                print(f"ไม่มีข้อมูล Gas={gas}, Year={current_year}")

        except requests.RequestException as e:
            print(f"Error fetching data for {gas}: {e}")
    
    # หากมีข้อมูลใหม่ให้บันทึกลงไฟล์
    if results:
        new_data = pd.concat(results, ignore_index=True)

        try:
            # อ่านไฟล์เดิม (ถ้ามี)
            existing_data = pd.read_csv("ClimateTraceArea.csv")
            
            # ลบข้อมูลที่ซ้ำกันตามปีและแก๊ส
            existing_data = existing_data[~((existing_data["year"] == current_year) & (existing_data["gas"].isin(gases)))]

            # รวมข้อมูลเก่าและใหม่
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        except (FileNotFoundError, pd.errors.EmptyDataError):
            combined_data = new_data

        # บันทึกข้อมูลที่อัปเดตลงในไฟล์ CSV
        combined_data.to_csv("ClimateTraceArea.csv", index=False)
        print("Data has been updated in ClimateTraceArea.csv")
    else:
        print("No new data to update.")
# urlCT()

def urlCT2():
    gases = ["co2e_100yr", "co2", "n2o", "ch4"]
    current_year = datetime.now().year  
    file_path = "ClimateTrace_Total.csv" 
    # ตรวจสอบปีที่มากที่สุดจากไฟล์ที่มีอยู่
    max_year_in_file = get_max_year(file_path)
    
    # ถ้าปีที่มากที่สุดในไฟล์ไม่เท่ากับปีปัจจุบัน ให้ดึงข้อมูลปีปัจจุบัน
    if max_year_in_file == current_year:
        print(f"ข้อมูลปี {current_year} มีอยู่แล้วในไฟล์")
        return

    results = []  # เก็บข้อมูลผลลัพธ์จาก API

    # ลูปดึงข้อมูลสำหรับแต่ละก๊าซ
    for gas in gases:
        url = f"https://api.c10e.org/v6/app/emissions?years={current_year}&gas={gas}&subsectors=&excludeForestry=true"
        
        try:
            # ส่งคำขอ GET ไปยัง API
            response = requests.get(url, timeout=30)  # เพิ่ม timeout เพื่อป้องกันการรอนานเกินไป
            response.raise_for_status()  # ตรวจสอบข้อผิดพลาดจาก HTTP

            # แปลงข้อมูล JSON ที่ได้รับจาก API
            json_data = response.json()

            # ถ้ามีข้อมูล "totals" สำหรับก๊าซในปีนี้
            if "totals" in json_data:
                total_value = json_data["totals"].get('value', 0)
                
                # ตรวจสอบว่าค่าผลรวมของก๊าซไม่เป็น 0
                if total_value != 0:
                    results.append({
                        'Gas': gas,  # ก๊าซ
                        'Year': current_year,  # ปี
                        'Total Value': total_value  # ผลรวมของก๊าซนั้นๆ
                    })
                    print(f"Gas: {gas}, Year: {current_year}, Total Value: {total_value}")
                else:
                    print(f"ข้อมูลของ Gas: {gas}, Year: {current_year} คือ 0, ยังไม่มีการอัพเดท...")
                    return  # หากค่าผลรวมเป็น 0 ให้หยุดการดำเนินการและรอ

        except requests.RequestException as e:
            print(f"Error fetching data for {gas}: {e}")

    # ถ้ามีข้อมูลใหม่ดึงมา
    if results:
        new_df = pd.DataFrame(results)  

        try:
            # อ่านข้อมูลจากไฟล์ CSV ที่มีอยู่แล้ว
            existing_df = pd.read_csv(file_path)
            # ลบข้อมูลที่มีปีปัจจุบันอยู่แล้วในไฟล์
            existing_df = existing_df[existing_df["Year"] != current_year]
            # รวมข้อมูลเก่าและใหม่
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)  
        except FileNotFoundError:
            # ถ้าไม่พบไฟล์เดิม ให้ใช้ข้อมูลใหม่ทั้งหมด
            updated_df = new_df  

        # บันทึกข้อมูลที่อัปเดตลงในไฟล์ CSV
        updated_df.to_csv(file_path, index=False)  
        print(f"ข้อมูลของ {current_year} อัพเดปแล้ว")
    else:
        print("ไม่มีการอัพเดป")
# urlCT2()

def urlCT3():
    current_year = datetime.now().year
    # URL สำหรับดาวน์โหลดไฟล์ CSV
    url = f"https://api.c10e.org/v6/country/emissions/timeseries/subsectors?since={current_year}&to={current_year}&download=csv&combined=false"
    
    # ตั้งค่า Chrome WebDriver
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    option.add_experimental_option("prefs", {"download.default_directory": download_folder})
    
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    
    # รอให้ดาวน์โหลดเสร็จ (เพิ่มความยืดหยุ่นในการรอไฟล์)
    time.sleep(10)  
    driver.quit()

    # ตรวจสอบไฟล์ที่ดาวน์โหลด
    downloaded_file = os.path.join(download_folder, f"trace_data_combined_false_since_{current_year}_to_{current_year}.csv")
    if not os.path.exists(downloaded_file):
        print("ไม่พบไฟล์ที่ดาวน์โหลด!")
        return
    
    # กำหนดไฟล์ปลายทาง
    target_folder = os.getcwd()
    target_file = os.path.join(target_folder, "trace_data_since_2015_to_2024_combined_false.csv")
    
    # อ่านข้อมูลใหม่จากไฟล์ที่ดาวน์โหลด
    new_data = pd.read_csv(downloaded_file)
    
    # ตรวจสอบว่ามีไฟล์ปลายทางอยู่แล้วหรือไม่
    if os.path.exists(target_file):
        existing_data = pd.read_csv(target_file)
        
        # เพิ่ม Timestamp ให้ข้อมูลเดิม
        existing_data['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # รวมข้อมูลและลบแถวที่ซ้ำกัน
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates(keep='last')
    else:
        # เพิ่ม Timestamp ให้ข้อมูลใหม่
        new_data['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        combined_data = new_data
    
    # บันทึกข้อมูลที่รวมลงในไฟล์ปลายทาง
    combined_data.to_csv(target_file, index=False)
    print(f"ข้อมูลถูกรวมและบันทึกที่: {target_file}")
    
    # ลบไฟล์ที่ดาวน์โหลด
    os.remove(downloaded_file)
    print(f"ไฟล์ที่ดาวน์โหลดถูกลบ: {downloaded_file}")
# urlCT3()