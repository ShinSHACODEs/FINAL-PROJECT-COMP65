import requests
import os
import shutil
from datetime import datetime
import pandas as pd
from selenium import webdriver
import time

def urlCW(source_ids, gas_ids, max_pages=200):
    # Define the base URL with placeholders
    base_URL = "https://www.climatewatchdata.org/api/v1/data/historical_emissions?source_ids[]=226&gas_ids[]=489&page=1&per_page=200&sector_ids[]=2641&sector_ids[]=2641&sort_col=2022&sort_dir=DESC"
    all_data = []
    page = 1

    while True:
        params = {
            "source_ids[]": source_ids,
            "gas_ids[]": gas_ids,
            "page": page,
            "per_page": 10000,
            "sort_col": "country",
            "sort_dir": "ASC"
        }

        try:
            # Make the request
            response = requests.get(base_URL, params=params)

            # Check if the request was successful
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                break

            data = response.json()

            # Check if the data is empty or invalid
            if not data.get("data"):
                print("No more data found.")
                break

            # Extend the all_data list with new data
            all_data.extend(data["data"])

            if page < max_pages:
                page += 1
            else:
                break
        except Exception as e:
            print(f"Error fetching data: {e}")
            break

    # If data was fetched, save it
    if all_data:
        df = pd.DataFrame(all_data)
        # Save the data as a CSV file
        file_name = f"ClimateWatchDATA.csv"
        df.to_csv(file_name, index=False)
        print(f"Data successfully saved to: {file_name}")
    else:
        print("No data to save.")

# Define the source and gas IDs
source_id = [214]
gas_id = [490, 491, 492, 493]

# Call the function to fetch and save data
urlCW(source_id, gas_id)

def fixyear():
# อ่านไฟล์ CSV
    climatewatch_data = pd.read_csv('ClimateWatchDATA.csv')
    climatewatch_data['emissions'] = climatewatch_data['emissions'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # ใช้ explode เพื่อแยกข้อมูลจาก 'emissions' ออกเป็นหลายแถว
    climatewatch_data_exploded = climatewatch_data.explode('emissions').reset_index(drop=True)

    # แยกคอลัมน์ 'year' และ 'value' จาก 'emissions'
    climatewatch_data_exploded[['year', 'value']] = pd.DataFrame(climatewatch_data_exploded['emissions'].tolist(), index=climatewatch_data_exploded.index)
    # ลบคอลัมน์ 'emissions'
    climatewatch_data_exploded.drop(columns=['emissions'], inplace=True)

    # รวมข้อมูลจากทั้งสอง DataFrame เก่า
    combined_data = pd.concat([climatewatch_data_exploded], ignore_index=True)

    # ลบแถวที่ซ้ำกัน
    combined_data.drop_duplicates(inplace=True)

    # บันทึกผลลัพธ์ลงในไฟล์ CSV
    combined_data.to_csv('ClimateWatchDATA.csv', index=False)
    print("\nข้อมูลถูกรวมและบันทึกลงในไฟล์ 'ClimateWatchDATA_Transformed_Updated.csv' แล้ว.")

fixyear()

#ฟังก์ชั่นดึงข้อมูลจากเว็บ Our world in Data ข้อมูล 1750 ถึง 2023 อนาคตสามารถรับเพิ่มได้เป็น API
def urlOWD():
    
    # URL สำหรับแต่ละประเภทของก๊าซเรือนกระจก
    urls = {
        "CO2": [
            "https://ourworldindata.org/grapher/cumulative-co-emissions.csv?v=1&csvType=full&useColumnShortNames=true",
            "https://ourworldindata.org/grapher/co-emissions-by-sector.csv?v=1&csvType=full&useColumnShortNames=true",
            "https://ourworldindata.org/grapher/co2-by-source.csv?v=1&csvType=full&useColumnShortNames=true",
        ],
        "CH4": [
            "https://ourworldindata.org/grapher/methane-emissions.csv?v=1&csvType=full&useColumnShortNames=true",
            "https://ourworldindata.org/grapher/methane-emissions-by-sector.csv?v=1&csvType=full&useColumnShortNames=true"
        ],
        "N2O": [
            "https://ourworldindata.org/grapher/nitrous-oxide-emissions.csv?v=1&csvType=full&useColumnShortNames=true",
            "https://ourworldindata.org/grapher/nitrous-oxide-emissions-by-sector.csv?v=1&csvType=full&useColumnShortNames=true"
        ]
    }
    
    dataframes = {}
    # กำหนดก๊าซชื่อก๊าซ แล้วให้ url เป็น urllist สำหรับเก็บเป็น item
    for gas, url_list in urls.items():
        dataframes[gas]= [pd.read_csv(urls, storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}) for urls in url_list]
        
    for gas, df in dataframes.items():
        # วนลูปในรายการ
        for i, df in enumerate(df):
            # print(df) 
            # print("=" * 50) 
                
            filename = f"{gas}_ourworld_{i+1}.csv"
            df.to_csv(filename, index=False)
# urlOWD()

# ฟังก์ชั่นดึงข้อมูลจากเว็บ Climate trace พื้นที่ตามจุดที่มีการเปิดเผย
def urlCT3():
    url = f"https://api.c10e.org/v6/country/emissions/timeseries/subsectors?since=2015&to=2024&download=csv&combined=false"
    
    # ตั้งค่า Chrome WebDriver
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    time.sleep(5)  # รอให้ดาวน์โหลดเสร็จ
    driver.quit()
    
    # ตรวจสอบไฟล์ที่ดาวน์โหลด
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    downloaded_file = [f for f in os.listdir(download_folder) if "trace" in f]
    
    # ถ้ามีไฟล์ที่ดาวน์โหลด
    if downloaded_file:
        # กำหนดที่อยู่ไฟล์ที่ดาวน์โหลดและปลายทาง
        downloaded_file_path = os.path.join(download_folder, downloaded_file[0])
        target_folder = os.path.join(os.getcwd())
        target_file = os.path.join(target_folder, "climatecountry.csv")
        
        # ย้ายไฟล์ไปยังที่อยู่ปลายทาง
        shutil.move(downloaded_file_path, target_file)
        print(f"ไฟล์ถูกย้ายไปที่: {target_file}")
    else:
        print("ไม่พบไฟล์ที่ดาวน์โหลด!")
# urlCT3()

def comapper():
    response = requests.get("https://api.carbonmapper.org/api/v1/catalog/plume-csv")
    if response.status_code == 200:
        with open("plume_data.csv", "wb") as file:
            file.write(response.content)
# comapper()

def urlCarMo():
     option = webdriver.ChromeOptions()
     option.add_experimental_option("detach", True)
     driver = webdriver.Chrome(options=option)
     driver.get("https://datas.carbonmonitor.org/API/downloadFullDataset.php?source=carbon_global")
     time.sleep(5)
     driver.quit()
# urlCarMo()
