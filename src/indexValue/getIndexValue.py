import requests
from bs4 import BeautifulSoup

def get_index_value():
    kospi_url = 'https://finance.naver.com/sise/sise_index.naver?code=KOSPI'
    response = requests.get(kospi_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    kospi_value = soup.select_one('#now_value').text
    
    kosdaq_url = 'https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ'
    response = requests.get(kosdaq_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    kosdaq_value = soup.select_one('#now_value').text
    
    dow_url = 'https://finance.naver.com/world/sise.naver?symbol=DJI@DJI'
    response = requests.get(dow_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    dow_value = soup.select_one('#content > div.rate_info > div.today > p.no_today > em').text.strip()
    
    nasdaq_url = 'https://finance.naver.com/world/sise.naver?symbol=NAS@IXIC'
    response = requests.get(nasdaq_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    nasdaq_value = soup.select_one('#content > div.rate_info > div.today > p.no_today > em').text.strip()
    
    sp500_url = 'https://finance.naver.com/world/sise.naver?symbol=SPI@SPX'
    response = requests.get(sp500_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    sp500_value = soup.select_one('#content > div.rate_info > div.today > p.no_today > em').text.strip()

    return kospi_value, kosdaq_value, dow_value, nasdaq_value, sp500_value