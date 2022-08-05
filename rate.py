from forex_python.converter import CurrencyRates
import requests
import json

def get_rate():
        rates = []
        # Get exchange rate from forex
        rates.append(get_rates_from_forex())

        # Get exchange rate from web various api
        url = 'https://v6.exchangerate-api.com/v6/c76df87bc570556626a1d437/latest/CAD'
        data = get_rates_from_api(url)
        rates.append(data['conversion_rates']['USD'])

        url = "https://api.manana.kr/exchange/rate/USD/CAD.json"
        data = get_rates_from_api(url)
        rates.append(data[0]["rate"])

        url = "https://openexchangerates.org/api/latest.json?app_id=4a3f292a06364b738e73798348159ce2&base=USD&symbols=CAD"
        data = get_rates_from_api(url)
        rates.append(1/data["rates"]["CAD"])

        return list_average(rates)


def get_rates_from_forex():
        c = CurrencyRates()
        return c.get_rate('CAD','USD')


def get_rates_from_api(url):
        response = requests.get(url)
        return response.json()


def list_average(list):
        return sum(list) / len(list)


if __name__ == '__main__':

        cur = get_rate()
        print (f"Current exchange rate is evaluated at {cur}")

