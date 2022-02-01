import pandas as pd
import requests
import urllib.parse
import datetime

wikipedia_pages = {
    'SPX': 'List of S&P 500 companies'
}

def get_revision_metadata(page, start_date=None, end_date=None, S=requests.Session(), **kwargs):
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "prop": "revisions",
        "titles": page,
        "rvprop": "ids|timestamp|user|comment",
        "rvslots": "main",
        "formatversion": "2",
        "format": "json",
        "rvlimit": 1,
        'rvdir': 'newer', # consistent with the intuitive notion start_date < end_date, useful if we want to get the oldest revision after some date
        # 'rvdir': 'older', # useful if we want to get the newest revision before some date
    }
    # optional params
    # note rvstart and rvend behave opposite the intuitive notion of start_date < end_date if using rvdir='older' - best to set rvstart and rvend explicitly through kwargs in this case
    if start_date is not None:
        PARAMS['rvstart'] = start_date.isoformat()
    if end_date is not None:
        PARAMS['rvend'] = end_date.isoformat()
    for k, v in kwargs.items():
        PARAMS[k] = v
    print('params')
    print(PARAMS)
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    print('Response:', DATA, flush=True)
    PAGES = DATA["query"]["pages"]
    revision = PAGES[0]['revisions'][0]
    return revision

def get_components_at(index: str = 'SPX', when: str = None):
    """
    Returns index components at a given date, according to the latest update on Wikipedia before the given date.
    Args:
        index (str): The index to get components for. Currently only 'SPX' is supported. Default = 'SPX'.
        when (str): The date when to search components. Default = today
    """
    if when is None:
        when = datetime.datetime.today()
    if isinstance(when, str):
        when = pd.to_datetime(when)
    when = when.isoformat()
    #when = str(when) # in case we are passed a date object
    #when += 'T00:00:00Z' # timestamp format expected by API
    #when = when.replace(' ', '')
    page = wikipedia_pages[index]
    revision = get_revision_metadata(page, rvdir='older', rvstart=when) # query results from 'when', moving in the 'older' direction (new->old); i.e. get newest result before 'when'
    print(f"Got results from {revision['timestamp']}")
    table = pd.read_html(f"https://en.wikipedia.org/w/index.php?title={urllib.parse.quote(page)}&oldid={revision['revid']}")
    #components_df = table[0]
    for df in table: # usually the components df will be table[0], but for some revisions the first table just holds comments about the article which we ignore
        if 'Symbol' in df.columns:
            df = df.set_index('Symbol')
            break
        elif 'Ticker symbol' in df.columns:
            df = df.set_index('Ticker symbol')
            df.index.name = 'Symbol'
            break
    return df.sort_index()

def get_components_history(index: str = 'SPX', start_date=None, end_date=None, freq='M'):
    """
    Get a list of historical components between start_date and end_date at the given frequency (e.g. monthly)
    Args:
        index (str):
        start_date:
        end_date:
        freq (str): pandas frequency string (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases)
    """
    if end_date is None:
        end_date = datetime.date.today()
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    historical_components = {}
    for date in dates:
        components_at_date = get_components_at(index=index, when=date)
        historical_components[str(date)] = list(components_at_date.index)
    return historical_components

if __name__ == '__main__':
    print('Get current components')
    sp500 = get_components_at(index='SPX')
    print(sp500.index, flush=True)
    print('Get historical components at October 2018')
    sp500_2015 = get_components_at(index='SPX', when='2018-10-01')
    print(sp500_2015.index, flush=True)
    print('Get historical components monthly since 2008') # before then, the list was not in table format
    sp500_monthly = get_components_history(index='SPX', start_date='2008-01-01', freq='M')
    sp500_monthly = pd.DataFrame.from_dict(sp500_monthly, orient='index')
    sp500_monthly.to_csv('sp500_monthly.csv')


