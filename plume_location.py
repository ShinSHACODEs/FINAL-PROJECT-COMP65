import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import gdown

# --- โหลดไฟล์ CSV จาก Google Drive ---
file_id = '1firkoPurXa3avZuVoafBgBs8S9mXNuyf'
url = f'https://drive.google.com/uc?id={file_id}'
gdown.download(url, 'location.csv', quiet=True)

# --- อ่าน CSV และเลือกเฉพาะคอลัมน์ที่ต้องการ ---
df = pd.read_csv('location.csv')
df = df[['plume_id', 'plume_latitude', 'plume_longitude']]

# --- สร้าง GeoDataFrame จุดพิกัดจาก longitude, latitude ---
geometry = [Point(xy) for xy in zip(df['plume_longitude'], df['plume_latitude'])]
gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# --- โหลด shapefile แผนที่โลกแบบ low-res จาก URL ---
url_shapefile = 'https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip'
world = gpd.read_file(url_shapefile)

# --- spatial join เช็คว่าจุดอยู่ในประเทศไหน ---
joined = gpd.sjoin(gdf_points, world, how="left", predicate='within')

# --- เพิ่มคอลัมน์ชื่อประเทศเป็นภาษาอังกฤษ ---
df['country'] = joined['NAME_EN']

# --- บันทึกไฟล์ CSV พร้อมคอลัมน์ country ---
df.to_csv('plume_with_country.csv', index=False)
os.remove('location.csv')

print("เสร็จสิ้น: บันทึกไฟล์ plume_with_country.csv พร้อมคอลัมน์ country (English)")
