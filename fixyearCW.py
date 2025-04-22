import pandas as pd
import ast

def fixyear():
# อ่านไฟล์ CSV
    # climatewatch_data = pd.read_csv('ClimateWatchDATA.csv')
    climatewatch_update = pd.read_csv('ClimateWatchUPDATE.csv')
    climatewatch_new = pd.read_csv('ClimateWatchDATA_Transformed.csv')
    
    # แปลงให้เป็นลิสต์ถ้ามีการใช้ string รูปแบบ list โดยใช้ ast.literal_eval()
    # climatewatch_data['emissions'] = climatewatch_data['emissions'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    climatewatch_update['emissions'] = climatewatch_update['emissions'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # ใช้ explode เพื่อแยกข้อมูลจาก 'emissions' ออกเป็นหลายแถว
    # climatewatch_data_exploded = climatewatch_data.explode('emissions').reset_index(drop=True)
    climatewatch_update_exploded = climatewatch_update.explode('emissions').reset_index(drop=True)

    # แยกคอลัมน์ 'year' และ 'value' จาก 'emissions'
    # climatewatch_data_exploded[['year', 'value']] = pd.DataFrame(climatewatch_data_exploded['emissions'].tolist(), index=climatewatch_data_exploded.index)
    climatewatch_update_exploded[['year', 'value']] = pd.DataFrame(climatewatch_update_exploded['emissions'].tolist(), index=climatewatch_update_exploded.index)

    # ลบคอลัมน์ 'emissions'
    # climatewatch_data_exploded.drop(columns=['emissions'], inplace=True)
    climatewatch_update_exploded.drop(columns=['emissions'], inplace=True)

    # รวมข้อมูลจากทั้งสอง DataFrame เก่า
    # combined_data = pd.concat([climatewatch_data_exploded ,climatewatch_update_exploded], ignore_index=True)
    # รวมข้อมูลจากทั้งสอง DataFrame
    combined_data = pd.concat([climatewatch_update_exploded, climatewatch_new], ignore_index=True)

    # ลบแถวที่ซ้ำกัน
    combined_data.drop_duplicates(inplace=True)

    # บันทึกผลลัพธ์ลงในไฟล์ CSV
    combined_data.to_csv('ClimateWatchDATA_Transformed.csv', index=False)
    print("\nข้อมูลถูกรวมและบันทึกลงในไฟล์ 'ClimateWatchDATA_Transformed_Updated.csv' แล้ว.")

fixyear()