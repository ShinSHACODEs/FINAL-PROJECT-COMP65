# 🌎 PSU Phuket Climate Data Project

This repository is part of **Project Computing 1 & 2**  
at **Prince of Songkla University, Phuket Campus** 🇹🇭  
The focus is on **Data Analytics, Data Visualization, and Automation** to analyze and visualize climate-related data.

---

## 🧭 Project Overview
- **Focus Areas:** Data Visualization, Data Analysis, Data Engineer, Business Intelligence
- **Academic Year:** 2024–2026 (พ.ศ. 2567–2569)  
- **Faculty:** College of Computing  
- **Major:** Computing
- **University:** Prince of Songkla University, Phuket Campus  

---

## 📂 Main Files and Structure

| File Type | Description | Example |
|------------|--------------|----------|
| **Original Data Extract** | Initial data extraction scripts | `Extract_code` |
| **Live Data Sources** | Updated data pulling scripts | `ClimateTrace`, `OurWorldData`, `CarbonMoni`, `carbonmapper` |
| **Weather Data** | Daily weather and temperature data | `Weather_data.py`, `tmd.py` |

> 📝 *Note:* The **Climate Watch** dataset has been removed from this version.

---

## 🧩 ER Diagram
![ER Diagram](https://github.com/user-attachments/assets/715c1214-c621-4c7b-afae-13eecf00e6c7)

---

## 🔄 Data Transformation Process
Data transformation and cleaning are performed using **Power BI Power Query**.

<img width="350" height="350" alt="Power Query Process" src="https://github.com/user-attachments/assets/30a9d82e-07c2-4906-a164-19c851ec9bcc" />

---

## ⚙️ GitHub Actions Automation
The project uses **GitHub Actions Workflow** to automatically extract and update climate data.

> 🔗 [See workflow configuration example here](https://github.com/ShinSHACODEs/Upload-file-to-Google-Drive)

---

## 📊 Power BI Dashboard
Explore the interactive data dashboard:  
👉 [https://shorturl.at/MHDv6](https://shorturl.at/MHDv6)

---

## 🌐 Web Application
Project webpage for climate data visualization:  
👉 [https://cutt.ly/psuphuketclimate](https://cutt.ly/psuphuketclimate)

<img width="1153" height="320" alt="Web Page Preview" src="https://github.com/user-attachments/assets/b4a1518b-64cf-4328-939d-a25ecdf7581a" />

---

## 🧰 Libraries Used

```python
# Web scraping & HTTP requests
import requests
from bs4 import BeautifulSoup

# Data manipulation
import pandas as pd

# Time & date handling
from datetime import datetime, timedelta
import time

# Web automation
from helium import start_firefox

# File management
import os, io, shutil
```

## Clone the Repository
```bash
git clone https://github.com/ShinSHACODEs/FINAL-PROJECT-COMP65.git
cd psu-phuket-climate
```

## Installs Requirements
pip install -r requirements.txt


🔁 GitHub Actions Workflow Example
name: Auto Extract Data

on:
  schedule:
    - cron: '0 0 * * *'  # Run every day at midnight
  workflow_dispatch:

jobs:
  extract:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Extract Script
        run: python Extract_code.py





