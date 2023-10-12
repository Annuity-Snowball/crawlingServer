import pandas as pd

def get_fear_greed_score(day, db):
    collection = db['fear_greed_score']
    cursor = collection .find({},{'_id':0})
    df_fear_greed = pd.DataFrame(list(cursor))
    
    fear_greed_score = df_fear_greed.loc[len(df_fear_greed)-day,'fear_greed_score']
    return fear_greed_score