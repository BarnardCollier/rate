import globals
import symbols
import bmo_accounts
import pandas as pd
import numpy as np
import rate

if __name__ == '__main__':

        holdings = symbols.get_tickers()
        exchange_rate = rate.get_rate()

        df_raw = bmo_accounts.read_account_info(globals.account_file)
        df = bmo_accounts.process_account_info(df_raw)
        df = bmo_accounts.stub_out(df,holdings)

        t = bmo_accounts.read_transactions(globals.transactions_file,holdings)

        buy=t[((t['Activity']=='Buy') | (t['Activity']=='Sell')) & (t['Symbol'].notnull())]
        tp = bmo_accounts.process_transactions(buy,holdings)
        df2 = pd.concat((df,tp))

	# need to correct for share symbols that do not match between BMO and Yahoo
        df2['Symbol'] = np.where(df2['Symbol'].str.match("CAR.UN.TO"),"CAR-UN.TO",df2['Symbol'])

        # save dataframe to csv file for possible export/import into yahoo finance
        df2.to_csv(globals.output_file, index=False, header=True, date_format="%Y%m%d")

        df2.reset_index(drop=True, inplace=True)
        df2['Cost']=df2['Quantity']*df2['Purchase Price']

        dividend = t[(t['Activity']=='Dividend')]['Total'].sum()
        dividend_CAD = t[(t['Activity']=='Dividend') & (t['CUR2']=="CAD")]['Total'].sum()
        dividend_US = dividend - dividend_CAD
        withhold = t[t['Activity']=='Misc cash']['Total'].sum()
        interest = t[t['Activity']=='Interest']['Total'].sum()
        interest_CAD = t[(t['Activity']=='Interest') & (t['CUR2']=="CAD")]['Total'].sum()
        interest_US = interest - interest_CAD
        fees = t[(t['Description'].str.contains("ARCHITECT FEE")) | (t['Description'].str.contains("MERIDIAN PROGRAM"))]['Total'].sum()
        total_cost_CAD = df2[df2['Symbol'].str.endswith('.TO')]['Cost'].sum()
        total_cost_US = df2[~df2['Symbol'].str.endswith('.TO')]['Cost'].sum()

        print("Account file: ", globals.account_file)
        print("Transaction file: ", globals.transactions_file)
        print("Output file: ", globals.output_file)
        print("Exchange rate: ", round(exchange_rate,6), "or (", round(1/exchange_rate,6), ")" )
        print("")
        print(f"Total CAD dividend received: {round(dividend_CAD,2):,} CAD")
        print(f"Total US dividend received: {round(dividend_US,2):,} USD")
        print(f"Total dividend received: {round(dividend_CAD+(dividend_US/exchange_rate),2):,} CAD")
        print(f"Total withholding fees: {round(withhold,2):,} USD")
        print(f"Total CAD interest received: {round(interest_CAD,2):,} CAD")
        print(f"Total US interest received: {round(interest_US,2):,} USD")
        print(f"Total interest received: {round(interest_CAD+(interest_US/exchange_rate),2):,} CAD")
        print(f"Total fees paid: {round(fees,2):,} CAD")
        print(f"Total CAD invested: {round(total_cost_CAD,2):,} CAD")
        print(f"Total US invested: {round(total_cost_US,2):,} USD")
        print(f"Total invested: {round(total_cost_CAD+(total_cost_US/exchange_rate),2):,} CAD")
