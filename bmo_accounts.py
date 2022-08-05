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
    df = pd.read_csv(file_name, skiprows=8, names=column_headers, header=0)
    return df

def process_account_info(df):
    # create pivot table to summarized by Symbol
    df_pivot = pd.pivot_table(df, values=['Quantity', 'Total_Cost'],
                              index=['Symbol'],
                              aggfunc={'Quantity': np.sum, 'Total_Cost': np.sum})
    df_out = df_pivot.rename(columns={"Quantity": "Quantity", "Total_Cost": "Cost"})
    # compute the unit price of the shares
    # useless comment only here to provoke a chnage in the docker build
    df_out['Purchase Price']=round(df_out['Cost']/df_out['Quantity'], 2)
    return df_out

def stub_out(df, holdings):
        df = pd.concat([df, holdings], axis=1)
        # add the stub fields so that the export to yahoo finance has all the data needed
        df['Current Price']=0
        df['Date']=pd.to_datetime('20220101')
        df['Time']=0
        df['Change']=0
        df['Open']=0
        df['High']=0
        df['Low']=0
        df['Volume']=0
        df['Trade Date']=pd.to_datetime('20220101')
        df['Commission']=0
        df['High Limit']=0
        df['Low Limit']=0
        df['Comment']='Test load for export to Yahoo'

        # change order to match the Yahoo import requirements
        df_out = df[['Ticker','Current Price','Date','Time','Change','Open','High','Low','Volume','Trade Date','Purchase Price','Quantity','Commission','High Limit','Low Limit','Comment']]
        df_out = df_out.rename(columns={"Ticker": "Symbol"})
        # remove any entry where the quantity is 0
        df_out = df_out[df_out.Quantity.notnull()]
        return df_out

def read_transactions(file_name, holdings):
        column_headers = ['Account', 'Nickname', 'Date', 'Activity', 'Description',
                          'Symbol', 'Price', 'CUR1', 'Quantity', 'Total', 'CUR2']
        df = pd.read_csv(file_name, skiprows=7, skipfooter=1, names=column_headers,
                         delimiter=',', header=0, engine='python', skip_blank_lines=True, na_filter=True)
        df.dropna(how="all", inplace=True)
        # delete lines where the Account number is blank
        # the following identifies all rows in the frame where the Account entry
        # is blank by converting it to a string (str) and removing all trailing spaces (strip) and
        # converting the result to a boolean: if any text exist in the column then the boolean is True (not 0)
        # but if the column is blank then the boolean is False (0)
        # the df[df structure] filters out the rows
        #print(df)
        #df = df[df['Account'].str.strip().astype(bool)]
        df.Quantity = df.Quantity.astype(float)
        df.Price = df.Price.astype(float)
        #df = pd.concat([df, holdings], axis=1)
        return df

def find_ticker(holdings, symbol):
        return holdings['Ticker'][symbol]

def process_transactions(df, holdings):
        df_pivot = pd.pivot_table(df, values=['Quantity', 'Total'],
                        index=['Symbol','Date','CUR1'],
                        aggfunc={'Quantity': np.sum, 'Total': np.sum})
        df_out = df_pivot.rename(columns={"Quantity": "Quantity", "Total": "Cost"})
        df_out.reset_index(inplace=True)
        df_out['Ticker'] = df_out.apply(lambda row: find_ticker(holdings,row['Symbol']), axis=1)
        df_out['Current Price']=0
        df_out['Trade Date']=pd.to_datetime(df_out['Date'])
        df_out['Date']=df_out['Trade Date']
        df_out['Time']=0
        df_out['Change']=0
        df_out['Open']=0
        df_out['High']=0
        df_out['Low']=0
        df_out['Volume']=0
        df_out['Purchase Price']=abs(round(df_out['Cost']/df_out['Quantity'], 2))
        df_out['Commission']=0
        df_out['High Limit']=0
        df_out['Low Limit']=0
        df_out['Comment']='Test load for export to Yahoo'
        df_out.rename(columns={"Ticker": "Symbol2"}, inplace=True)
        df_out2 = df_out[['Symbol2','Current Price','Date','Time','Change','Open','High','Low','Volume','Trade Date','Purchase Price','Quantity','Commission','High Limit','Low Limit','Comment']]
        df_out2.rename(columns={"Symbol2": "Symbol"}, inplace=True)
        return df_out2
