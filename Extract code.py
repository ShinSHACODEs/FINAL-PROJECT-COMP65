# Source Extraction
import requests
import os
import shutil
from datetime import datetime
import pandas as pd
from ctrace.constants import * # จากเว็บ https://tjhunter.github.io/climate-trace-handbook/initial_analysis.html#country-emissions
from selenium import webdriver
import time
 
#ปีเก่าสุดของ CT
def start_yearforCT(data=None, default_year=2021):
    if data and "year" in data:
        return min(data["year"])
    else:
        return default_year

#ฟังก์ชั่นการทำงานของการดึงข้อมูล ของเว็บ ClimateWatch  ข้อมูล 1990 ถึง 2021
def urlCW(source_id, gas_id, max_pages=200):
    base_URL = "https://www.climatewatchdata.org/api/v1/data/historical_emissions"
    all_data = []
    page = 1

    while True:
        params = {
            "source_ids[]": source_id,
            "gas_ids[]": gas_id,
            "page": page,
            "per_page": 10000,
            "sort_col": "country" ,
            "sort_dir": "ASC"
        }
        response = requests.get(base_URL, params=params)
        data = response.json()

        if not data.get("data"):
            break

        all_data.extend(data["data"])

        if page < max_pages:
            page += 1
        else:
            break

    # แปลงข้อมูลเป็น DataFrame
    df = pd.DataFrame(all_data)
    
    # บันทึกข้อมูลเป็น CSV
    df.to_csv("ClimateWatchDATA.csv", index=False)
    print("บันทึกข้อมูลเรียบร้อย: ClimateWatchDATA.csv")

source_id = [214, 215, 216, 217]
gas_id = [474, 475, 476, 477]  
# urlCW(source_id, gas_id)



    # # แยกข้อมูล emissions ออกเป็น year และ value
    # emissions_expanded = df.explode("emissions").reset_index(drop=True)
    # emissions_expanded[["year", "value"]] = emissions_expanded["emissions"].apply(lambda x: pd.Series(x))

    # # ลบคอลัมน์ emissions เดิม
    # emissions_expanded.drop("emissions", axis=1, inplace=True)

    # # เลือกเฉพาะคอลัมน์ที่ต้องการ
    # result_df = emissions_expanded[["country", "iso_code3", "data_source", "sector", "gas", "year", "value"]]


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
def urlCT():
    # Define gases and years
    gases = ["co2e_100yr", "co2", "n2o", "ch4"]
    current_year = datetime.now().year
    years = list(range(start_yearforCT(), current_year))

    results = []

    for gas in gases:
        for year in years:
            url = f"https://api.c10e.org/v6/app/assets?year={year}&gas={gas}&subsectors="
            response = requests.get(url)

            if response.status_code == 200:
                json_data = response.json()

                if "assets" in json_data and json_data["assets"]:
                    df = pd.DataFrame(json_data["assets"])
                    df["year"] = year  # Add the year column
                    df["gas"] = gas  # Add the gas column
                    results.append(df)
                    print(f"Fetched: Gas={gas}, Year={year}")

    if results:
        final_df = pd.concat(results, ignore_index=True)
        final_df.to_csv("ClimateTraceArea.csv", index=False)
        print("Data saved to ClimateTraceArea.csv")
# urlCT()

# รับเอาค่าที่มากที่สุดแต่ละปีีมา
def urlCT2():
    gases = ["co2e_100yr", "co2", "n2o", "ch4"]
    current_year = datetime.now().year
    years = list(range(start_yearforCT(), current_year))  # ข้อมูลจาก api มีถึงแค่ 2021
    
    results = []  

    for gas in gases:
        for year in years:
            url = f"https://api.c10e.org/v6/app/emissions?years={year}&gas={gas}&subsectors=&excludeForestry=true"
            response = requests.get(url)
            json_data = response.json()
            
            if "totals" in json_data:
                total = json_data["totals"]
                # Append the total data to the results list
                results.append({
                    'Gas': gas,
                    'Year': year,
                    'Total Value': total['value']
                })
                print(f"Gas: {gas}, Year: {year}, Total Value: {total['value']}")
    df = pd.DataFrame(results)
    df.to_csv("ClimateTrace_Total.csv", index=False)  
# urlCT2()   

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
        target_file = os.path.join(target_folder, "trace_data_since_2015_to_2024_combined_false.csv")
        
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
