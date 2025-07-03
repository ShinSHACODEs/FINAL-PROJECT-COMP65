import requests
import pandas as pd
import io
import shutil
import os

def comapper():
    url = "https://api.carbonmapper.org/api/v1/catalog/plume-csv"
    response = requests.get(url)
    if response.status_code == 200:
        read_file = pd.read_csv(io.StringIO(response.text))        
        file_name = "plume_data.csv"
        read_file.to_csv(file_name, index=False)
    else:
        print("โหลดข้อมูลไม่สำเร็จ")

def readcsv():
    try:
        df = pd.read_csv('plume_data.csv')
        
        columns_to_drop = [
            'plume_bounds', 'instrument', 'mission_phase', 'emission_cmf_type', 
            'emission_version', 'processing_software', 'gsd', 'sensitivity_mode', 
            'off_nadir', 'published_at', 'wind_direction_std_auto', 'wind_source_auto', 
            'platform', 'provider', 'plume_tif', 'plume_png', 'con_tif', 'rgb_tif', 'rgb_png'
        ]
        df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
        df.drop_duplicates(inplace=True)

        os.remove('plume_data.csv')

        cleaned_file = 'plume_data_cleaned.csv'
        unique_key = 'plume_id'

        if os.path.exists(cleaned_file):
            existing_df = pd.read_csv(cleaned_file)
            new_data = df[~df[unique_key].isin(existing_df[unique_key])]

            if new_data.empty:
                print("ไม่มีข้อมูลใหม่")
            else:
                combined_df = pd.concat([existing_df, new_data], ignore_index=True)
                combined_df.to_csv(cleaned_file, index=False)
        else:
            df.to_csv(cleaned_file, index=False)
            print(f"สร้างไฟล์ใหม่ {cleaned_file} → มีทั้งหมด {len(df)} แถว")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

comapper()
readcsv()
