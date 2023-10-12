import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

today = datetime.today()
yesterday = today - timedelta(days=1)
days_ago_300 = yesterday - timedelta(days=300)
days_ago_3 = yesterday - timedelta(days=3)
yesterday = yesterday.strftime("%Y%m%d")
days_ago_300 = days_ago_300.strftime("%Y%m%d")
days_ago_3  = days_ago_3.strftime("%Y%m%d")

def get_bond_data(temp_path):
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    prefs = {"download.default_directory" : temp_path}
    chromeOptions.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(options=chromeOptions)

    driver.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC020104040402")

    time.sleep(5)

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

    search_btn = driver.find_element(By.CSS_SELECTOR, '#MDCSTAT115_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD > img')
    search_btn.click()
    rand = random.randrange(2, 4)
    time.sleep(rand)

    search_btn = driver.find_element(By.CSS_SELECTOR, '#ui-id-1 > div > div:nth-child(2) > a')
    search_btn.click()
    rand = random.randrange(4, 6)
    time.sleep(rand)

    driver.quit()