import requests
from bs4 import BeautifulSoup

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
measurement()

def tem():
    url = "https://climate.nasa.gov/vital-signs/global-temperature/?intent=121"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    primary = soup.find('div', class_='latest_measurement')
    
    latest = primary.find('div', class_='value').get_text(strip=True)
    # จัดรูปแบบผลลัพธ์
    latest = latest.replace("°C", "°C ")
    print(f"ค่าล่าสุดผิดปกติ global-temperature: {latest}")  
tem()


