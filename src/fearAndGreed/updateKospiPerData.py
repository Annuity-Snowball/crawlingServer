import os
import pandas as pd

def update_kospi_per_data(db, temp_path):
    collection = db['kospi_per']

    cursor = collection .find({},{'_id':0})
    df_origin = pd.DataFrame(list(cursor))
    

    last_date = df_origin.iloc[-1]['Date'] 
    print(last_date)
    print()
    file_list = os.listdir(temp_path)
    file_list.sort()
    df_temp = pd.read_csv(temp_path+"/"+file_list[0], encoding='cp949')
    print(df_temp.info())
    print(df_temp.head())
    
    df_temp['Date'] = pd.to_datetime(df_temp['일자'], format='%Y/%m/%d')
    df_temp = df_temp.sort_values(by=['Date'])
    
    result = pd.concat([df_origin, df_temp], ignore_index=True)
    result = result.sort_values(by=['Date'])
    result = result.drop_duplicates(subset=['Date'])
    result = result.loc[result['Date']>last_date,:]
    result = result.dropna()
    result = result.reset_index(drop=True)
    
    if result.empty:
        pass
    else:
        upload_documents = result.to_dict("records")
        result = collection.insert_many(upload_documents)
    
    os.remove(temp_path+"/"+file_list[0])