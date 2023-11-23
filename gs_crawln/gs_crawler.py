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


def gs_crawling(search_command, stop_year, override, override_url):

    driver = get_driver()

    # search_command = "Kuan-Yu Chen umich"
    # stop_year = 2015

    print(f"Name : {search_command}, Until : {stop_year}")
    url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C23&q=" + search_command + "&btnG="

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
            journal_field = driver.find_elements(By.CLASS_NAME, 'gsc_oci_field')[2].text
            if journal_field == "Description":
                journal = " "
                continue
            else:
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

    current_year = time.ctime().split()[-1]

    for i in range(int(current_year), int(stop_year), -1):
        print(f"[[{i} - {search_command.split()[1]}]]", file=file)
    print('-------------------------------------------------------------------------------------------------------------------------',file=file)


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

        if "ISCA" in journal_list[i]:
            journal_tmp = "ISCA"
        elif "International Symposium on Computer Architecture" in journal_list[i]:
            journal_tmp = "ISCA"
        elif "Micro" in journal_list[i]:
            journal_tmp = "Micro"
        elif "MICRO" in journal_list[i]:
            journal_tmp = "Micro"
        elif "HPCA" in journal_list[i]:
            journal_tmp = "HPCA"
        elif "ASAP" in journal_list[i]:
            journal_tmp = "ASAP"
        elif "IISWC" in journal_list[i]:
            journal_tmp = "IISWC"
        elif "HCS" in journal_list[i]:
            journal_tmp = "HCS"
        elif "PACT" in journal_list[i]:
            journal_tmp = "PACT"
        elif "ISPASS" in journal_list[i]:
            journal_tmp = "ISPASS"
        elif "FCCM" in journal_list[i]:
            journal_tmp = "FCCM"
        elif "ICCD" in journal_list[i]:
            journal_tmp = "ICCD"
        elif "MWSCAS" in journal_list[i]:
            journal_tmp = "MWSCAS"
        elif "ISSCC" in journal_list[i]:
            journal_tmp = "ISSCC"
        elif "Symposium on VLSI Circuits" in journal_list[i]:
            journal_tmp = "VLSI"
        elif "IEEE Journal of Solid-State Circuits" in journal_list[i]:
            journal_tmp = "JSSC"
        elif "CICC" in journal_list[i]:
            journal_tmp = "CICC"
        elif "DAC" in journal_list[i]:
            journal_tmp = "DAC"
        elif "A-SSCC" in journal_list[i]:
            journal_tmp = "A-SSCC"
        elif "ESSCIRC" in journal_list[i]:
            journal_tmp = "ESSCIRC"
        elif "DATE" in journal_list[i]:
            journal_tmp = "DATE"
        elif "ISLPED" in journal_list[i]:
            journal_tmp = "ISLPED"
        elif "arXiv" in journal_list[i]:
            journal_tmp = "arXiv"
        else:
            journal_tmp = journal_list[i]

        print("[[", journal_tmp, "]]", sep='', file=file)
        print('-------------------------------------------------------------------------------------------------------------------------', file=file)

    file.close()
    print("Crawling is complete ! ")


if __name__ == '__main__':

    argv = sys.argv
    search_command = argv[1] + " " + argv[2]

    if(len(argv) >= 4):
        stop_year = argv[3]
    else:
        stop_year = '2015'

    if(len(argv) >= 5):
        override = int(argv[4])
        override_url = argv[5].strip('"')
    else:
        override = 0
        override_url = ''

    print(override, override_url)
    print(search_command)
    print(stop_year)




    gs_crawling(search_command, stop_year, override, override_url)

