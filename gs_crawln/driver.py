from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time



chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(2)

search_command = "David Blaauw"
url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C23&q=" + search_command + "&btnG="
driver.get(url)

#time.sleep(10)

#search_url = driver.find_elements(By.CLASS_NAME, "gs_rt2")

links = "#gs_res_ccl_mid > div:nth-child(1) > table > tbody > tr > td:nth-child(2) > h4 > a"

search_url = driver.find_elements(By.CSS_SELECTOR, links)

print("주소: ", search_url.get_attribute("href"))

print("Hi")




#driver.close()

