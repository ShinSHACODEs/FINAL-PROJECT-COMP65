import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def measurement():
    name = ["Carbon Dioxide","Methane"]
    for item in name:
        
        url = f"https://climate.nasa.gov/vital-signs/{item.replace(' ', '-').lower()}/?intent=121"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        primary_column = soup.find('div', class_='latest_measurement')
        
        latest_measurement = primary_column.find('div', class_='value').get_text(strip=True)
        date = primary_column.find('span', class_='no_wrap').get_text(strip=True)
        
        # Print the result in a single line without extra blank lines
        print(f"ค่าล่าสุด: {item}: {latest_measurement}, วันเวลา: {date}")
# measurement()

def tem():
    url = "https://climate.nasa.gov/vital-signs/global-temperature/?intent=121"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    primary = soup.find('div', class_='latest_measurement')
    
    latest = primary.find('div', class_='value').get_text(strip=True)
    # จัดรูปแบบผลลัพธ์
    latest = latest.replace("°C", "°C ")
    print(f"ค่าล่าสุดผิดปกติ global-temperature: {latest}")  
# tem()

def tmd():
    options = Options()
    driver = webdriver.Chrome(options=options)
    url = "https://www.tmd.go.th/climate/daily"
    driver.get(url)

    time.sleep(10)
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[5]/div/div[3]/div/div/div/table')))
        climate_data = driver.find_elements(By.XPATH, '/html/body/main/div/div[5]/div/div[3]/div/div/div/table/tbody/tr')

        # ดึงข้อมูลเมื่อวาน
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y')

        # สร้างรายการเพื่อเก็บข้อมูลจากแต่ละแถว
        rows = []
        for data in climate_data:
            columns = data.find_elements(By.TAG_NAME, "td")
            row = [col.text for col in columns]
            rows.append(row + [yesterday])  # เพิ่มคอลัมน์วันที่

        # สร้าง DataFrame จากข้อมูลที่ดึงมา
        df = pd.DataFrame(rows, columns=["สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ", "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี", "วันที่"])

        # บันทึกข้อมูลลง CSV
        df.to_csv("TMDdata.csv", index=False, encoding="utf-8-sig")
        print("บันทึกข้อมูลสำเร็จ: TMDdata.csv")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

    finally:
        driver.quit()

# เรียกใช้งานฟังก์ชัน
tmd()



def weather():
    url = "https://www.timeanddate.com/weather/?low=4&sort=1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    primary = soup.find('div', class_="tb-scroll")
    data = []
    for row in primary.findAll('tr'):
        cells = row.find_all('td')
        row_data = [cell.get_text(strip=True) for cell in cells]
        if row_data:
            data.append(row_data)

    # สร้าง DataFrame จากข้อมูลที่ดึงมา
    df = pd.DataFrame(data, columns=["Country-City","Date","img","Temperature"])
    df.drop(["img"], axis=1, inplace=True) 
    df.to_csv("weatherdata.csv", index=False, encoding="utf-8-sig")
    print(df)
# weather()