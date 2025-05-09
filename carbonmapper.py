import requests
import pandas as pd
import io
import shutil
import os
import gdown

def comapper():
    url = "https://api.carbonmapper.org/api/v1/catalog/plume-csv"
    response = requests.get(url)
    if response.status_code == 200:
        read_file = pd.read_csv(io.StringIO(response.text))        
        file_name = "plume_data.csv"
        read_file.to_csv(file_name, index=False)
        shutil.move(file_name, os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name))
        print("ย้ายไฟล์สำเร็จ")
comapper()

def readcsv():
    try:
        df = pd.read_csv('plume_data.csv')
        columns_to_drop = [
            'plume_bounds', 'instrument', 'mission_phase', 'emission_cmf_type', 
            'emission_version', 'processing_software', 'gsd', 'sensitivity_mode', 
            'off_nadir', 'published_at', 'wind_direction_std_auto', 'wind_source_auto', 
            'platform', 'provider', 'plume_tif', 'plume_png', 'con_tif', 'rgb_tif', 'rgb_png'
        ]
        df.drop(columns=columns_to_drop, inplace=True)
        df.drop_duplicates(inplace=True)

                # อ่านไฟล์เก่า
        file_id = "1avgQR_ZpHmsLILLQUpdwKMAXt1aNEsTP"
        url2 = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url2, "plume_data_cleaned.csv", quiet=False)
        cleaned_file = 'plume_data_cleaned.csv'
        
        if os.path.exists(cleaned_file):
            existing_df = pd.read_csv(cleaned_file)
            combined_df = pd.concat([existing_df, df]).drop_duplicates()
            if len(combined_df) == len(existing_df) + len(df):
                print("ไม่มีข้อมูลซ้ำ")
            else:
                print("มีข้อมูลซ้ำ")
            combined_df.to_csv(cleaned_file, index=False)
        else:
            df.to_csv(cleaned_file, index=False)
            print("บันทึกไฟล์ใหม่")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
readcsv()
