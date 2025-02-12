# Source Extraction
import requests
import pandas as pd
import ctrace as ct #pip install climate-trace, #pip install huggingface_hub
from ctrace.constants import * # จากเว็บ https://tjhunter.github.io/climate-trace-handbook/initial_analysis.html#country-emissions

#ฟังก์ชั่นการทำงานของการดึงข้อมูล ของเว็บ ClimateWatch
def urlCW(source_id, gas_id,max_pages=200):
    base_URL = "https://www.climatewatchdata.org/api/v1/data/historical_emissions"
    all_data = []
    page = 1

    # อ่านค่า sector_id และ id_gas จากไฟล์มีให้้ใช้ในเว็บ
    while True:
        params = {
            "source_ids[]": source_id,
            "gas_ids[]": gas_id,
            "page": page,
            "per_page": 10000,
            "sort_col": "country",
            "sort_dir": "ASC"
        }
        response = requests.get(base_URL,params=params)
        data = response.json()
        
        #if เช็คหากไม่มีข้อมูลในdata ให้หยุด
        if not data.get("data"):
            break
        all_data.extend(data["data"]) 
        
        #ทำjsonให้เป็นมาตราฐานให้กลายเป็นตาราง
        df = pd.json_normalize(data["data"])
        print(df) 
        
        #if ถ้าเลขหน้าpageน้อยกว่าmaxpageให้ปริ้นหน้าต่อไป หากหมดให้หยุด
        if page < max_pages:
            page += 1
        else:
            break
    final_df = pd.json_normalize(all_data)
    final_df.to_csv("ClimateWatchDATA.csv", index=False)   
source_id = [214,215,216,217]
gas_id = [474,475,476,477]        
# urlCW(source_id, gas_id)

#ฟังก์ชั่นดึงข้อมูลจากเว็บ Our world in Data
def urlOWD():
    # URL สำหรับแต่ละประเภทของก๊าซเรือนกระจก
    urls = {
        "CO2": [
            "https://ourworldindata.org/grapher/cumulative-co-emissions.csv?v=1&csvType=full&useColumnShortNames=true",
            "https://ourworldindata.org/grapher/co-emissions-by-sector.csv?v=1&csvType=full&useColumnShortNames=true",
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
    # ใช้for ดึงข้อมูล
    # กำหนดก๊าซชื่อก๊าซ แล้วให้ url เป็น urllist สำหรับเก็บเป็น item
    for gas, url_list in urls.items():
        dataframes[gas]= [pd.read_csv(urls, storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}) for urls in url_list]
        
    for gas, df in dataframes.items():
        # วนลูปในรายการ
        for i, df in enumerate(df):
            print(df) 
            print("=" * 50) 
            filename = f"{gas}_data_file_{i+1}.csv"
            df.to_csv(filename, index=False)
# urlOWD()


#ฟังก์ชั่นดึงข้อมูลจากเว็บ Our world in Data พื้นที่ตามจุดที่มีการเปิดเผย
def urlCT():
    gases = ["co2e_100yr","co2", "n2o", "ch4"]
    years = [2021, 2022, 2023, 2024]
    
    for gas in gases:
        for year in years:
            url = f"https://api.c10e.org/v6/app/assets?year={year}&gas={gas}&subsectors="
            response = requests.get(url)
            json_data = response.json()
            df = pd.json_normalize(json_data["assets"])
            print(f"Gas: {gas}, Year: {year}")
            print(df)
            
    # #ตัวที่สองที่เจอ
    # cedf = ct.read_country_emissions(GAS_LIST)
    # print(cedf)
# urlCT()

#รับเอาค่าที่มากที่สุดแต่ละปีีมา
def urlCT2():
    gases = ["co2e_100yr","co2", "n2o", "ch4"]
    years = [2021, 2022, 2023, 2024]
    
    for gas in gases:
        for year in years:
            url = f"https://api.c10e.org/v6/app/emissions?years={year}&gas={gas}&subsectors=&excludeForestry=true"
            response = requests.get(url)
            json_data = response.json()
            
            if "totals" in json_data:
                total = json_data["totals"]
                print(f"Gas: {gas}, Year: {year}, Total Value: {total['value']}")
# urlCT2()

# หาทางเอาค่า แต่ละประเทศหรือภูมิภาค
def urlCT3():


