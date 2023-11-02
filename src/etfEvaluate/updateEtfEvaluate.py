import pandas as pd
import pymongo
import numpy as np

def update_etf_evaluate(db):

    collection = db['etf_finance'] 
    cursor = collection .find({},{'_id':0})
    df_etf_finance = pd.DataFrame(list(cursor))

    collection = db['etf_price']  # 여기서 'mycollection'은 사용하려는 컬렉션 이름입니다.
    cursor = collection .find({},{'_id':0})
    df_etf_closing_price = pd.DataFrame(list(cursor))
    
    collection = db['etf_evaluate']
    result = collection.find_one(sort=[("etf_date", pymongo.DESCENDING)])
    etf_evaluate_last_date = result['etf_date']
    
    df_etf_closing_price = df_etf_closing_price[['etf_code', 'etf_price','etf_date']]
    
    df_etf_closing_price = df_etf_closing_price.sort_values(['etf_date'])
    df_etf_finance = df_etf_finance.sort_values(['pdf_date'])
    
    df_etf_finance = pd.merge_asof(df_etf_closing_price, df_etf_finance, by='etf_code',left_on='etf_date', right_on = 'pdf_date')
    df_etf_finance = df_etf_finance.drop(columns='pdf_date')
    
    df_etf_evaluate = df_etf_finance.loc[df_etf_finance['etf_revenue'].notnull(),:]
    
    df_etf_evaluate['etf_per'] = df_etf_evaluate['etf_price']  / df_etf_evaluate['etf_profitloss']
    df_etf_evaluate['etf_pbr'] = df_etf_evaluate['etf_price']  / df_etf_evaluate['etf_equity']
    df_etf_evaluate['etf_psr'] = df_etf_evaluate['etf_price']  / df_etf_evaluate['etf_revenue']

    df_etf_evaluate['etf_operating_ratio'] = 100*(df_etf_evaluate['etf_operatingincomeloss']/df_etf_evaluate['etf_revenue'])
    df_etf_evaluate['etf_profit_ratio'] = 100*(df_etf_evaluate['etf_profitloss']/df_etf_evaluate['etf_revenue'])
    df_etf_evaluate['etf_debt_ratio'] = 100*(df_etf_evaluate['etf_liabilities']/df_etf_evaluate['etf_equity'])
    df_etf_evaluate['etf_roe']= 100*(df_etf_evaluate['etf_profitloss']/df_etf_evaluate['etf_equity'])

    df_etf_evaluate = df_etf_evaluate.sort_values(['etf_code','etf_date'])
    df_etf_evaluate = df_etf_evaluate.reset_index(drop=True)
    
    df_etf_evaluate.loc[df_etf_evaluate['etf_per']<0,'etf_per'] = np.inf
    
    df_etf_evaluate_month = df_etf_evaluate[['etf_code','etf_date','etf_price','etf_revenue','etf_operatingincomeloss','etf_profitloss']].copy()

    # etf_date에서 한 달 후의 연도와 월을 추출하여 새로운 컬럼들을 추가
    df_etf_evaluate_month['match_year'] = (df_etf_evaluate_month['etf_date'] + pd.DateOffset(months=1)).dt.year
    df_etf_evaluate_month['match_month'] = (df_etf_evaluate_month['etf_date'] + pd.DateOffset(months=1)).dt.month
        
    df_etf_evaluate_month = df_etf_evaluate_month.groupby(['etf_code', 'match_year','match_month']).agg({
    'etf_price': 'mean',
    'etf_revenue': 'mean',
    'etf_operatingincomeloss': 'mean',
    'etf_profitloss': 'mean'
    })
    df_etf_evaluate_month = df_etf_evaluate_month.reset_index()
    df_etf_evaluate_month = df_etf_evaluate_month.rename(columns={'etf_price':'last_month_etf_price','etf_revenue': 'last_month_etf_revenue','etf_operatingincomeloss':'last_month_etf_operatingincomeloss',
                                                                'etf_profitloss': 'last_month_etf_profitloss'})
    
    df_etf_evaluate['etf_year'] = df_etf_evaluate['etf_date'].dt.year
    df_etf_evaluate['etf_month'] = df_etf_evaluate['etf_date'].dt.month
    
    df_etf_evaluate = pd.merge(df_etf_evaluate, df_etf_evaluate_month, how='left', left_on = ['etf_code','etf_year','etf_month'], right_on = ['etf_code','match_year','match_month'] )
    
    df_etf_evaluate = df_etf_evaluate.loc[df_etf_evaluate['match_year'].notnull(),:]
    
    for index,row in df_etf_evaluate.iterrows():
        
        df_etf_evaluate.loc[index,'etf_price_change'] = (100*(df_etf_evaluate.loc[index,'etf_price'] -  df_etf_evaluate.loc[index,'last_month_etf_price'])) / df_etf_evaluate.loc[index,'last_month_etf_price']

        df_etf_evaluate.loc[index,'etf_revenue_change'] = (100*(df_etf_evaluate.loc[index,'etf_revenue'] -  df_etf_evaluate.loc[index,'last_month_etf_revenue'])) / df_etf_evaluate.loc[index,'last_month_etf_revenue']

        df_etf_evaluate.loc[index,'etf_operatingincomeloss_change'] = (100*(df_etf_evaluate.loc[index,'etf_operatingincomeloss'] -  df_etf_evaluate.loc[index,'last_month_etf_operatingincomeloss'])) / df_etf_evaluate.loc[index,'last_month_etf_operatingincomeloss']

        df_etf_evaluate.loc[index,'etf_profitloss_change'] = (100*(df_etf_evaluate.loc[index,'etf_profitloss'] -  df_etf_evaluate.loc[index,'last_month_etf_profitloss'])) / df_etf_evaluate.loc[index,'last_month_etf_profitloss']
    
    
    df_etf_evaluate = df_etf_evaluate.drop(columns=['etf_year', 'etf_month','match_year',	'match_month',	'last_month_etf_price',	'last_month_etf_revenue',	'last_month_etf_operatingincomeloss',	'last_month_etf_profitloss'])
    df_etf_evaluate = df_etf_evaluate.loc[df_etf_evaluate['etf_date']>etf_evaluate_last_date,:]
    df_etf_evaluate = df_etf_evaluate.reset_index(drop=True)
        
    if pd.isnull(df_etf_evaluate.loc[0,'etf_price']):
        pass
    else:
        upload_documents = df_etf_evaluate.to_dict("records")

        result = collection.insert_many(upload_documents)