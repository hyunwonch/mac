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
import warnings
warnings.filterwarnings("ignore")


def get_driver():
    print("Get Chrome Driver")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    return driver


def get_url(driver, url):
    try:
        driver.get(url)
    except:
        driver.close()


def gs_crawling(search_command, stop_year):

    driver = get_driver()

    # search_command = "Kuan-Yu Chen umich"
    # stop_year = 2015

    print(f"Name : {search_command}, Until : {stop_year}")
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C23&q=" + search_command + "&btnG="

    override_url = "https://scholar.google.com/citations?user=6tBFbCQAAAAJ&hl=en"
    override = 0
    end_signal = 0

    if (override):
        get_url(driver, override_url)
        driver.find_element(By.XPATH, '//*[@id="gsc_a_ha"]').click()
        time.sleep(5)
    else:
        get_url(driver, url)

        # Go to actual link that contains list
        time.sleep(5)
        try:
            driver.find_element(By.XPATH, '//*[@id="gs_res_ccl_mid"]/div[1]/table/tbody/tr/td[2]/h4/a').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="gsc_a_ha"]').click()
            time.sleep(5)
        except:
            try:
                driver.find_element(By.XPATH, '//*[@id="gs_res_ccl_mid"]/div[1]/table/tbody/tr/td[2]/div[1]/h4/a').click()
                time.sleep(2)
                driver.find_element(By.XPATH, '//*[@id="gsc_a_ha"]').click()
                time.sleep(5)
            except:
                driver.close()
                end_signal = 1

    # Show more button
    while(1):
        if(driver.find_element(By.XPATH, '//*[@id="gsc_bpf_more"]').get_attribute('disabled')):
            break
        driver.find_element(By.XPATH, '//*[@id="gsc_bpf_more"]').click()
        time.sleep(1)

    # Get all paper links
    print("Get links of each paper")
    paper_link_list = []
    num = 1
    while(True):
        link = '#gsc_a_b > tr:nth-child(' + str(num) + ') > td.gsc_a_t > a'
        try:
            paper_link = driver.find_elements(By.CSS_SELECTOR, link)[0].get_attribute("href")
        except:
            break
        num += 1
        paper_link_list.append(paper_link)

    print("The Number of papers :", len(paper_link_list))

    # Save the information

    title_list = []
    authors_list = []
    date_list = []
    journal_list = []

    print("Get the information of each paper")
    for i in paper_link_list:
        driver.get(i)
        try:
            title = driver.find_element(By.CLASS_NAME, 'gsc_oci_title_link').text
            authors = driver.find_elements(By.CLASS_NAME, 'gsc_oci_value')[0].text
            date = driver.find_elements(By.CLASS_NAME, 'gsc_oci_value')[1].text
            journal = driver.find_elements(By.CLASS_NAME, 'gsc_oci_value')[2].text
            #print(title)
            #print(authors)
            #print(date)
            #print(journal)
            if(date.split('/')[0] == stop_year):
                break
            title_list.append(title)
            authors_list.append(authors)
            date_list.append(date)
            journal_list.append(journal)
            time.sleep(5)
        except:
            continue
    driver.close()

    new_authors_list = []
    for i in authors_list:
        tmp = i.split(",")
        tmp_list = []
        for j in tmp:
            tmp_list.append("[[" + j.strip() + "]]")
        new_authors_list.append(tmp_list)
    #print(new_authors_list[0])

    print("Total Length : ", len(title_list))

    file_name = "./paper_list/" + search_command + ".txt"
    print(file_name)
    file = open(file_name,'w')

    for i in range(len(title_list)):
        if(journal_list[i] == 'US'):
            continue
        print(date_list[i], file=file)
        print("[[", title_list[i], "]]", sep='', file=file)
        for index, j in enumerate(new_authors_list[i]):
            if(index == (len(new_authors_list[i])-1)):
                print(j,"", sep='', end='\n', file=file)
            else:
                print(j,", ", sep='', end='', file=file)
        print(journal_list[i], file=file)
        print('-------------------------------------------------------------------------------------------------------------------------', file=file)

    file.close()
    print("Crawling is complete ! ")


if __name__ == '__main__':

    argv = sys.argv
    # search_command = "Dejan Markovic"
    search_command = argv[1] + " " + argv[2]

    if(len(argv) == 4):
        stop_year = argv[3]
    else:
        stop_year = '2018'

    print(search_command)
    print(stop_year)




    gs_crawling(search_command, stop_year)

