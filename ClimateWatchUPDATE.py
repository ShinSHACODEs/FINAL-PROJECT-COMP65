import pandas as pd
import time
from datetime import datetime
import requests
import pandas as pd
import json

# ข้อมูลใหม่ของ CliamteWatch

def max_year(filename="ClimateWatchDATA.csv"):
    try:
        df = pd.read_csv(filename)

        # แปลงคอลัมน์ emissions เป็น list ของ dict หากเป็น string
        def parse_emissions(emissions):
            try:
                return json.loads(emissions.replace("'", '"')) if isinstance(emissions, str) else emissions
            except json.JSONDecodeError:
                return []
        
        df["emissions"] = df["emissions"].apply(parse_emissions)
        
        # ดึงค่าปีจาก emissions
        all_years = [year_data.get("year") for sublist in df["emissions"] if isinstance(sublist, list) for year_data in sublist if "year" in year_data]
        
        if all_years:
            return max(all_years)
        else:
            return None
    except FileNotFoundError:
        print(f"ไม่พบไฟล์ {filename}")
        return None

def urlCW(source_id, gas_id, max_pages=200):
    base_URL = "https://www.climatewatchdata.org/api/v1/data/historical_emissions"
    all_data = []
    page = 1
    start_year = max_year() 
    end_year = datetime.now().year

    while True:
        params = {
            "source_ids[]": source_id,
            "gas_ids[]": gas_id,
            "page": page,
            "per_page": 10000,
            "start_year": start_year,
            "end_year": end_year,
            "sort_col": "country",
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
    
    # ลบแถวที่มีค่า None หรือ NaN
    df = df.dropna().reset_index(drop=True)
    
    # บันทึกข้อมูลเป็น CSV
    df.to_csv("ClimateWatchUPDATE.csv", index=False)
    print("บันทึกข้อมูลเรียบร้อย: ClimateWatchDATA.csv")

source_id = [214, 215, 216, 217]
gas_id = [474, 475, 476, 477]  
urlCW(source_id, gas_id)
