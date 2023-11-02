import time
import random
import shutil
import os
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

today = datetime.today()
yesterday = today - timedelta(days=1)
days_ago_300 = yesterday - timedelta(days=300)
days_ago_3 = yesterday - timedelta(days=3)
yesterday = yesterday.strftime("%Y%m%d")
days_ago_300 = days_ago_300.strftime("%Y%m%d")
days_ago_3  = days_ago_3.strftime("%Y%m%d")


def get_etf_price(db, temp_path):
    collection = db['etf_price']

    cursor = collection .find({},{'_id':0})
    df_etf_price = pd.DataFrame(list(cursor))

    last_date = df_etf_price.iloc[-1]['etf_date'] 

    today = datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    date_list = []

    current_date = last_date + timedelta(days=1)
    
    print(current_date, today)
    
    while current_date < today:
        date_list.append(current_date.strftime('%Y%m%d'))
        current_date += timedelta(days=1)
        
    for product_date in date_list:
        chromeOptions = Options()
        # chromeOptions.add_argument("--headless")
        prefs = {"download.default_directory" : temp_path}
        chromeOptions.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(options=chromeOptions)

        driver.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030101")

        rand = random.randrange(3, 6)
        time.sleep(rand)

        search_btn = driver.find_element(By.CSS_SELECTOR,'#trdDd') 
        search_btn.click()
        rand = random.randrange(2, 4)
        time.sleep(rand)
        search_btn.send_keys(Keys.COMMAND + 'a')
        rand = random.randrange(2, 4)
        time.sleep(rand)
        search_btn.send_keys((Keys.BACKSPACE))
        rand = random.randrange(2, 4)
        time.sleep(rand)
        search_btn.send_keys(product_date)
        rand = random.randrange(2, 4)
        time.sleep(rand)

        search_btn = driver.find_element(By.CSS_SELECTOR, '#jsSearchButton')
        search_btn.click()
        rand = random.randrange(3, 6)
        time.sleep(rand)

        search_btn = driver.find_element(By.CSS_SELECTOR, '#MDCSTAT043_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > button.CI-MDI-UNIT-DOWNLOAD > img')
        search_btn.click()
        rand = random.randrange(3, 6)
        time.sleep(rand)
        search_btn = driver.find_elements(By.CLASS_NAME, 'ico_filedown')
        search_btn[1].click()
        time.sleep(2)
        
        filename = max([temp_path + "/" + f for f in os.listdir(temp_path)], key=os.path.getctime)
        shutil.move(filename, os.path.join(temp_path, "ETF_" + product_date + ".csv"))
        time.sleep(1)
        
        driver.quit()