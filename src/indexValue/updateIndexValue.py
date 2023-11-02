def update_index_value(redis_client, kospi_value, kosdaq_value, dow_value, nasdaq_value, sp500_value):
    data = {
        "kospi": kospi_value,
        "kosdaq": kosdaq_value,
        "dow": dow_value,
        "nasdaq": nasdaq_value,
        "sp500": sp500_value
    }
    
    if redis_client.exists('index_value'):
        redis_client.json().set('iv:index_value', '.', data)
    else:
        redis_client.json().set('iv:index_value', '$', data)
        
def update_yesterday_value(redis_client, kospi_value, kosdaq_value, dow_value, nasdaq_value, sp500_value):
    data = {
        "kospi": kospi_value,
        "kosdaq": kosdaq_value,
        "dow": dow_value,
        "nasdaq": nasdaq_value,
        "sp500": sp500_value
    }
    
    if redis_client.exists('index_value'):
        redis_client.json().set('iv:yesterday_value', '.', data)
    else:
        redis_client.json().set('iv:yesterday_value', '$', data)