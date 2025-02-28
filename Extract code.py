# Source Extraction
import requests
from datetime import datetime
import pandas as pd
import ctrace as ct #pip install climate-trace, #pip install huggingface_hub
from ctrace.constants import * # จากเว็บ https://tjhunter.github.io/climate-trace-handbook/initial_analysis.html#country-emissions
from bs4 import BeautifulSoup
from selenium import webdriver
import time
 
#ปีเก่าสุดของ CT
def start_yearforCT(data=None, default_year=2021):
    if data and "year" in data:
        return min(data["year"])
    else:
        return default_year

#ฟังก์ชั่นการทำงานของการดึงข้อมูล ของเว็บ ClimateWatch  ข้อมูล 1990 ถึง 2021
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
        df = pd.DataFrame.from_dict(data["data"]) # pd.json_normalize() เปลี่ยนเป็น pd.DataFrame.from_dict()
        # print(df) 
        
        #if ถ้าเลขหน้าpageน้อยกว่าmaxpageให้ปริ้นหน้าต่อไป หากหมดให้หยุด
        if page < max_pages:
            page += 1
        else:
            break
    final_df = pd.DataFrame.from_dict(all_data)
    final_df.to_csv("ClimateWatchDATA.csv", index=False)   
source_id = [214,215,216,217]
gas_id = [474,475,476,477]        
# urlCW(source_id, gas_id)

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
    #กำหนด gas และ year เป็น list สำหรับใช้ใน lurl
    gases = ["co2e_100yr", "co2", "n2o", "ch4"]
    current_year = datetime.now().year
    years = list(range(start_yearforCT(),current_year))  # ข้อมูลจาก api มีถึงแค่ 2021
    results = []

    for gas in gases:
        for year in years:
            url = f"https://api.c10e.org/v6/app/assets?year={years}&gas={gas}&subsectors="
            response = requests.get(url)
            json_data = response.json()
            
            if "assets" in json_data:
                df = pd.DataFrame.from_dict(json_data["assets"])
                results.append(df)
                print(f"Gas: {gas}, Year: {year}")
    final_df = pd.concat(results, ignore_index=True)
    final_df.to_csv("ClimateTraceArea.csv", index=False)  
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
    # df.to_csv("ClimateTrace_Total.csv", index=False)  
urlCT2()   

#Selenium รอแก้ใน ปีถัดไปได้
def urlCT3():
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=option)
    driver.get("https://api.c10e.org/v6/country/emissions/timeseries/subsectors?since=2015&to=2024&download=csv&combined=false")
    time.sleep(5)
    driver.quit()
# urlCT3()

# def urlCarMo(): # ได้ไหม?
#     option = webdriver.ChromeOptions()
#     option.add_experimental_option("detach", True)
#     driver = webdriver.Chrome(options=option)
#     driver.get("https://datas.carbonmonitor.org/API/downloadFullDataset.php?source=carbon_global")
#     time.sleep(5)
#     driver.quit()
# # urlCarMo()

# def urlEdgar(): #ลิงค์อาจไม่รองรับในอนาคตต
#     option = webdriver.ChromeOptions()
#     option.add_experimental_option("detach", True)
#     driver = webdriver.Chrome(options=option)
#     driver.get("https://edgar.jrc.ec.europa.eu/booklet/EDGAR_2024_GHG_booklet_2024.xlsx")
#     time.sleep(5)
#     driver.quit()
# # urlEdgar()
