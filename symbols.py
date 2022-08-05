import globals
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None

def read_account_info(file_name):
    column_headers = ['Account', 'Nickname', 'Asset Class', 'Asset Type', 'Type', 'Currency', 'Symbol',
                      'Description', 'DSC',
                      'Quantity', 'Unit_Cost', 'CUR0', 'Cost Status', 'Total Cost', 'CUR1', 'Previous Close',
                      'Price Ind', 'CUR2', 'Total_Cost',
                      'CUR3', 'Yield', 'Unrealized Gain/Loss', 'CUR4', 'Gain/Loss']
    df = pd.read_csv(file_name, skiprows=8, names=column_headers, header=0, usecols=['Symbol','CUR0'])
    return df

def read_transactions(file_name):
    column_headers = ['Account', 'Nickname', 'Date', 'Activity', 'Description',
                      'Symbol', 'Price', 'CUR1', 'Quantity', 'Total', 'CUR0']
    df = pd.read_csv(file_name, skiprows=7, skipfooter=1, names=column_headers,
                     delimiter=',', header=0, engine='python', skip_blank_lines=True, na_filter=True, usecols=['Symbol','CUR0'])
    df.dropna(how="all", inplace=True)
    return df

def find_ticker(symbol, currency):
    if (currency == "CAD"):
       value = symbol + ".TO"
    else:
       value = symbol
    return value

def get_tickers():
    s = read_account_info(globals.account_file)
    t = read_transactions(globals.transactions_file)
    #d = s.append(t)
    d = pd.concat((s,t))
    d = d[d['Symbol'].notnull()]
    d = d.dropna()
    d = d.drop_duplicates()
    d['Ticker'] = d.apply(lambda row: find_ticker(row['Symbol'],row['CUR0']), axis=1)
    d = d[['Symbol','Ticker']]
    d.set_index('Symbol',drop=True, inplace=True)
    return d

if __name__ == '__main__':
    d = get_tickers()
    print(d)
