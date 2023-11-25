from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import os
import sys
import time
import subprocess
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")



def get_citation(name):
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C23&q=" + name
    res = requests.get(url)
    res.raise_for_status()  # 정상 200
    soup = BeautifulSoup(res.text, "lxml")

    cited_by_elem = soup.find('div', {'class': 'gs_flb'})


    if cited_by_elem:
        # Extract the number of citations
        citations_text = cited_by_elem.find_all('a')
        print(f"Citation : {citations_text[2].text.split()[-1]}")


get_citation("Statistical timing analysis for intra-die process variations with spatial correlations")