# Library จำเป็นสำหรับ Project

import requests
from datetime import datetime
import pandas as pd
import ctrace as ct #pip install climate-trace, #pip install huggingface_hub
from ctrace.constants import * # จากเว็บ https://tjhunter.github.io/climate-trace-handbook/initial_analysis.html#country-emissions
from bs4 import BeautifulSoup
from selenium import webdriver
import time
