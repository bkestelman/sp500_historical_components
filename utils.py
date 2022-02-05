import pandas as pd

def isoformat(date):
    date = pd.to_datetime(date)
    return date.isoformat()
