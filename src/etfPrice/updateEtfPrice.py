import os
import pandas as pd

def update_etf_price(db, temp_path):
    collection = db['etf_price']

    file_list = os.listdir(temp_path)
    file_list.sort()

    for file_name in file_list[0:]:
        date_str = file_name.split('.')[0].split('_')[1]

        df = pd.read_csv(temp_path+'/'+file_name,encoding='cp949')
        df = df[['종목코드','종목명','종가','시가총액']]
        df['etf_date'] = date_str
        df['etf_date'] = pd.to_datetime(df['etf_date'],format='%Y%m%d')
        df.rename(columns={'종목코드': 'etf_code', '종목명': 'etf_name',
                                                '종가': 'etf_price', '시가총액':'etf_total_price'}, inplace=True)

        if pd.isnull(df.loc[0,'etf_price']):
            continue
        else:
            upload_documents = df.to_dict("records")

            result = collection.insert_many(upload_documents)
    for file_name in file_list[0:]:
        os.remove(temp_path+"/"+file_name)