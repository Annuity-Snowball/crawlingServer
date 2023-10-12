import time
import pytz
import configparser
import redis
from pymongo import MongoClient
from datetime import datetime
import sys
sys.path.append('/Users/gimsangsu/Desktop/mainF/school/project/graduateProject/backend/crawlingServer')
from src.etfPrice.getEtfPrice import get_etf_price
from src.etfPrice.updateEtfPrice import update_etf_price
from src.fearAndGreed.getBondData import get_bond_data
from src.fearAndGreed.getFearGreedScore import get_fear_greed_score
from src.fearAndGreed.getKospiPerData import get_kospi_per_data
from src.fearAndGreed.getPutCallData import get_put_call_data
from src.fearAndGreed.updateBondData import update_bond_data
from src.fearAndGreed.updateKospiPerData import update_kospi_per_data
from src.fearAndGreed.updatePutCallData import update_put_call_data
from src.fearAndGreed.makeFearGreedScore import make_fear_greed_score
from src.indexValue.getIndexValue import get_index_value
from src.indexValue.updateIndexValue import update_index_value

config = configparser.ConfigParser()

config.read("/Users/gimsangsu/Desktop/mainF/school/project/graduateProject/backend/crawlingServer/src/config/mongodb-config.ini")

host = config['mongo']['host']
port = int(config['mongo']['port'])

client = MongoClient(host, port)
db = client['snowball_data_engineer']

config.read("/Users/gimsangsu/Desktop/mainF/school/project/graduateProject/backend/crawlingServer/src/config/redis-config.ini")

redis_host = config['redis']['host']
redis_port = int(config['redis']['port'])

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

temp_path = "/Users/gimsangsu/Desktop/mainF/school/project/graduateProject/backend/crawlingServer/temp"
    
if __name__ == "__main__":
    while True:
        current_time = datetime.now(pytz.timezone('Asia/Seoul'))
        current_hour_str = current_time.strftime("%H")
        current_minute_str = current_time.strftime("%M")
        current_second_str = current_time.strftime("%S")
        print(current_second_str)
        if (current_hour_str =='22') and (current_minute_str =='39'):
            get_kospi_per_data(temp_path)
            update_kospi_per_data(db, temp_path)
            get_put_call_data(temp_path)
            update_put_call_data(db, temp_path)
            get_bond_data(temp_path)
            update_bond_data(db, temp_path)     
            get_etf_price(db, temp_path)
            update_etf_price(db, temp_path)
            make_fear_greed_score(db)
            
            yesterday_fear_greed_score = get_fear_greed_score(1, db)
            day7_fear_greed_score = get_fear_greed_score(7, db)
            day30_fear_greed_score = get_fear_greed_score(30, db)
            day180_fear_greed_score = get_fear_greed_score(180, db)
            day365_fear_greed_score = get_fear_greed_score(365, db)
            
            print('어제 공포탐욕 점수', yesterday_fear_greed_score)
            print('7일전 공포탐욕 점수', day7_fear_greed_score)
            print('30일전 공포탐욕 점수', day30_fear_greed_score)
            print('180일전 공포탐욕 점수', day180_fear_greed_score)
            print('365일전 공포탐욕 점수', day365_fear_greed_score)
        
        elif int(current_second_str) % 5 == 0:
            kospi_value, kosdaq_value, dow_value, nasdaq_value, sp500_value = get_index_value()
            update_index_value(
                redis_client=redis_client,
                kospi_value=kosdaq_value,
                kosdaq_value=kosdaq_value,
                dow_value=dow_value,
                nasdaq_value=nasdaq_value,
                sp500_value=sp500_value
            )
            print('코스피 :', kospi_value)
            print('코스닥 :', kosdaq_value)
            print('다우존스 :', dow_value)
            print('나스닥 :', nasdaq_value)
            print('s&p500 :', sp500_value)             
            
        else:
            time.sleep(1)