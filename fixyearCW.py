import pandas as pd
def fixyear():
    # อ่านไฟล์ CSV
    climatewatch_data = pd.read_csv('ClimateWatchDATA.csv')
    climatewatch_update = pd.read_csv('ClimateWatchUPDATE.csv')
    
    climatewatch_data['emissions'] = climatewatch_data['emissions'].apply(lambda x: eval(x) if isinstance(x, str) else x)  # แปลงให้เป็นลิสต์ถ้ามีการใช้ string รูปแบบ list

    # ใช้ explode เพื่อแยกข้อมูลจาก 'emissions' ออกเป็นหลายแถว
    climatewatch_data_exploded = climatewatch_data.explode('emissions').reset_index(drop=True)
    climatewatch_data_exploded[['year', 'value']] = pd.DataFrame(climatewatch_data_exploded['emissions'].tolist(), index=climatewatch_data_exploded.index)
    climatewatch_data_exploded.drop(columns=['emissions'], inplace=True)

    # บันทึกผลลัพธ์ลงในไฟล์ CSV
    climatewatch_data_exploded.to_csv('ClimateWatchDATA_Transformed.csv', index=False)
    print("\nข้อมูลถูกบันทึกลงในไฟล์ 'ClimateWatchDATA_Transformed.csv' แล้ว.")
fixyear()
