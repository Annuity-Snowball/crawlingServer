import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def make_fear_greed_score(db):
    collection = db['fear_greed_score']
    collection.drop()
    
    collection = db['kospi_per']
    cursor = collection .find({},{'_id':0})
    df_kospi = pd.DataFrame(list(cursor))
    
    df_kospi = df_kospi[['Date','종가','PER']]
    df_kospi = df_kospi.reset_index(drop=True)

    for cal_index in range(124,len(df_kospi)):
        start_index = cal_index-124
        sum_value = 0
        for i in range(start_index, cal_index+1):
            sum_value += df_kospi.loc[i]['종가']

        df_kospi.loc[cal_index,'125days_kospi_index'] = sum_value/125

    for cal_index in range(124,len(df_kospi)):
        start_index = cal_index-124
        sum_value = 0
        for i in range(start_index, cal_index+1):
            sum_value += df_kospi.loc[i]['PER']

        df_kospi.loc[cal_index,'125days_per'] = sum_value/125

    for cal_index in range(19,len(df_kospi)):
        start_index = cal_index-19
        df_kospi.loc[cal_index,'20days_kospi_index_change_rate'] = 100*((df_kospi.loc[cal_index,'종가'] - df_kospi.loc[start_index,'종가'])/df_kospi.loc[start_index,'종가'])

    collection = db['put_call']
    cursor = collection .find({},{'_id':0})
    df_put_call = pd.DataFrame(list(cursor))
        
    df_final= pd.merge(df_kospi, df_put_call[['Date','P/C Ratio']], on='Date')

    collection = db['korean_bond']
    cursor = collection .find({},{'_id':0})
    df_bond = pd.DataFrame(list(cursor))
    
    df_bond = df_bond.rename(columns={'10년물_금리': '10year_bond_rate'})
    df_final= pd.merge(df_final, df_bond[['Date','10year_bond_rate']], on='Date')
    df_fear_greed = pd.DataFrame()
    
    df_fear_greed['Date'] = df_final['Date']
    df_fear_greed['kospi_index'] = df_final['종가']
    df_fear_greed['kospi_momentum'] = df_final['125days_kospi_index'] - df_final['종가']
    df_fear_greed['p/c_ratio'] = df_final['P/C Ratio']
    df_fear_greed['safe_demand'] = df_final['10year_bond_rate'] - df_final['20days_kospi_index_change_rate']
    df_fear_greed['per_momentum'] = df_final['125days_per'] - df_final['PER']

    scaler = MinMaxScaler(feature_range=(0, 25))

    kospi_momentum_normalized = scaler.fit_transform(df_fear_greed[['kospi_momentum']])
    p_c_ratio_normalized = scaler.fit_transform(df_fear_greed[['p/c_ratio']])
    safe_demand_normalized = scaler.fit_transform(df_fear_greed[['safe_demand']])
    per_momentum_normalized = scaler.fit_transform(df_fear_greed[['per_momentum']])

    df_fear_greed['kospi_momentum_normalized'] = kospi_momentum_normalized
    df_fear_greed['p_c_ratio_normalized'] = p_c_ratio_normalized
    df_fear_greed['safe_demand_normalized'] = safe_demand_normalized
    df_fear_greed['per_momentum_normalized'] = per_momentum_normalized

    df_fear_greed['fear_greed_score'] = df_fear_greed['kospi_momentum_normalized'] + df_fear_greed['p_c_ratio_normalized'] + df_fear_greed['safe_demand_normalized'] +  df_fear_greed['per_momentum_normalized']

    df_fear_greed['fear_greed_score'] = df_fear_greed['fear_greed_score'].round(0).astype(int)

    collection = db['fear_greed_score']
    upload_documents = df_fear_greed.to_dict("records")
    result = collection.insert_many(upload_documents)