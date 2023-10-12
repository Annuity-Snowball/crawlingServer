import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
days_ago_300 = yesterday - timedelta(days=300)
days_ago_3 = yesterday - timedelta(days=3)
yesterday = yesterday.strftime("%Y%m%d")
days_ago_300 = days_ago_300.strftime("%Y%m%d")
days_ago_3  = days_ago_3.strftime("%Y%m%d")

def get_kospi_per_data(temp_path):
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    prefs = {"download.default_directory" : temp_path}
    chromeOptions.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(options=chromeOptions)

    driver.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010107")

    time.sleep(5)

    label = driver.find_element(By.CSS_SELECTOR, '#MDCSTAT007_FORM > div.search_tb > div > table > tbody > tr:nth-child(1) > td > label:nth-child(4)')
    label.click()
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#tboxindTpCd_finder_equidx0_0')
    rand = random.randrange(2, 4)
    time.sleep(rand)
    search_btn.send_keys(Keys.RETURN)
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#searchText__finder_equidx0_0')
    search_btn.send_keys('코스피')
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#searchBtn__finder_equidx0_0')
    search_btn.click()
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#jsGrid__finder_equidx0_0 > tbody > tr:nth-child(1) > td.tal.pl20')
    search_btn.click()
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#strtDd') 
    search_btn.click()
    search_btn.clear()
    search_btn.send_keys(days_ago_300)
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#endDd') 
    search_btn.click()
    search_btn.clear()
    search_btn.send_keys(yesterday)
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR,'#jsSearchButton')
    search_btn.click()
    rand = random.randrange(4, 6)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR, '#MDCSTAT007_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD > img')
    search_btn.click()
    rand = random.randrange(2, 4)
    time.sleep(rand)
    
    search_btn = driver.find_element(By.CSS_SELECTOR, '#ui-id-3 > div > div:nth-child(2) > a')
    search_btn.click()
    rand = random.randrange(4, 6)
    time.sleep(rand)

    driver.quit()