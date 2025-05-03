from datetime import datetime, timedelta
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def tmd():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    url = "https://www.tmd.go.th/climate/daily"
    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//table[contains(@class, "table")]')))
        time.sleep(5)

        climate_data = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        rows = []

        for data in climate_data:
            columns = data.find_elements(By.TAG_NAME, "td")
            row = [col.text.strip() for col in columns]
            if len(row) == 8:
                row.append(yesterday)
                rows.append(row)

        df_new = pd.DataFrame(rows, columns=[
            "สถานีอุตุนิยมวิทยา", "อุณหภูมิสูงสุด", "อุณหภูมิต่ำสุด", "ทิศ",
            "ความเร็ว (กม./ชม.)", "เวลา", "ปริมาณฝน มม.", "รวมตั้งแต่ต้นปี", "วันที่"
        ])

        df_new.to_csv("TMDdata.csv", index=False, encoding="utf-8-sig")
        print("บันทึกข้อมูลใหม่สำเร็จ: TMDdata.csv")

    finally:
        driver.quit()

tmd()
