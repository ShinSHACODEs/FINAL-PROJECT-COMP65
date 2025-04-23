import pandas as pd
import os

# ฟังก์ชันหาปีที่มากที่สุดจากคอลัมน์ 'Year'
def start_yearfor(data=None):
    if data is not None and "Year" in data.columns:
        return data["Year"].max()
    else:
        print("Not found")
        return None

# ฟังก์ชั่นดึงข้อมูลจากเว็บ Our World in Data
def urlOWD():

    # URLs สำหรับแต่ละก๊าซ
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

    # ดึงข้อมูลจาก URL
    for gas, url_list in urls.items():
        for i, url in enumerate(url_list):
            filename = f"{gas}_ourworld_{i+1}.csv"
            
            # โหลดข้อมูลใหม่จาก URL
            try:
                new_df = pd.read_csv(url, storage_options={'User-Agent': 'Our World In Data data fetch/1.0'})
            except Exception as e:
                continue

            # โหลดข้อมูลเก่า (ถ้ามี)
            if os.path.exists(filename):
                try:
                    existing_df = pd.read_csv(filename)
                except Exception as e:
                    continue

                # หาปีที่มากที่สุดจากข้อมูลเก่า
                max_year_existing = start_yearfor(existing_df)

                # กรองข้อมูลใหม่เฉพาะปีที่ยังไม่มีในข้อมูลเก่า
                new_df = new_df[new_df["Year"] > max_year_existing]

                # ถ้าข้อมูลใหม่ว่างเปล่า ให้ข้ามไป
                if new_df.empty:
                    print(f"ไม่มีข้อมูลใหม่สำหรับ {filename}")
                    continue

                # รวมข้อมูลเก่าและใหม่
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                updated_df.to_csv(filename, index=False)
                print(f"เพิ่มข้อมูลใหม่ลงใน {filename}")
            else:
                # ถ้าไฟล์ไม่มีอยู่แล้ว ให้สร้างใหม่
                new_df.to_csv(filename, index=False)
                print(f"สร้างไฟล์ใหม่: {filename}")
urlOWD()
