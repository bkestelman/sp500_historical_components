"""
Compare our components to fja05680's
"""
import pandas as pd
from datetime import date

def main():
    max_num_components = 510 # TODO: shouldn't be a magic number
    NAN_TOKEN = 'NaN Token'
    multiclass_shares_format = '-'
    # read our components
    our_csv = 'sp500_monthly.csv'
    our_components = pd.read_csv(our_csv, index_col=0, parse_dates=[0])
    our_components.index.name = 'date'
    #our_components.index = pd.to_datetime(our_components.index)
    our_components.index = our_components.index.date.astype('datetime64[ns]')
    #our_components.index = our_components.index.date + pd.offsets.MonthEnd(0)
    our_components = our_components.fillna(NAN_TOKEN)
    format_multiclass_shares(our_components, use_format=multiclass_shares_format)
    print(our_components)
    # read fja's components
    their_csv = 'fja05680_sp500.csv'
    their_components = pd.read_csv(their_csv, index_col=0, parse_dates=[0], names=range(max_num_components))
    their_components.index.name = 'date'
    their_components = their_components.fillna(NAN_TOKEN)
    print(their_components)
    format_multiclass_shares(their_components, use_format=multiclass_shares_format)
    print(their_components)
    # group by month, get last, set date to match last day of month
    their_components['date'] = their_components.index
    print(their_components)
    their_components = their_components.groupby([their_components.index.year, their_components.index.month]).last()
    their_components = their_components.set_index('date')
    print('index after groupby')
    print(their_components.index)
    #their_components.index = pd.to_datetime(their_components.index.levels[0]
    print('after groupby month, last()')
    print(their_components)
    their_components.index = their_components.index + pd.offsets.MonthEnd(0)
    print('adjsuted dates for their components to match ours')
    print(their_components)
    print(their_components.index)
    print(our_components.index)
    # for date in our, for comp in our for comp in fja
    for i in range(len(our_components)):
        our_row = our_components.iloc[i]
        their_row = their_components.loc[our_row.name]
        print(f'Comparing our row with their row for {our_row.name}')
        print('in our row but not in their row')
        for comp in our_row:
            if comp not in their_row.values and comp != NAN_TOKEN:
                print(comp)
        print('in their row but not in our row')
        for comp in their_row:
            if comp not in our_row.values and comp != NAN_TOKEN:
                print(comp)

def format_multiclass_shares(df, use_format='-'):
    if use_format == '-':
        old_format = '.'
    if use_format == '.':
        old_format = '-'
    for col in df.columns:
        df[col] = df[col].str.replace(old_format, use_format, regex=False)

if __name__ == '__main__':
    main()
