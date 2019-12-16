import pandas as pd
import datetime
import requests
import json
from datetime import datetime
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_fullprice(ticker, terms='max'):
    url = 'https://api.coingecko.com/api/v3/coins/' + \
        ticker + '/market_chart?vs_currency=jpy&days=' + terms
    r = requests.get(url)
    r2 = json.loads(r.text)
    return r2


def get_price(r2):
    s = pd.DataFrame(r2['prices'])
    s.columns = ['date', 'price']
    date = []
    for i in s['date']:
        tsdate = int(i/1000)
        loc = datetime.utcfromtimestamp(tsdate)
        date.append(loc)
    s.index = date
    del s['date']
    return s


def get_lastprice(ticker, currency, only_price, vol24='true', change24='true'):
    """[bitcoinの価格を取得する関数]
    上の関数は前から使っているので一応残しているだけで
    こっちの方が処理速度とかが早いのでこれかあはこちらを使うことが推奨

    only_price -価格のみを返す
    FALSEにした場合は価格出来高24時間変化率を返す
    """

    ticker_data = cg.get_price(
        ids=ticker, vs_currencies=currency,
        include_24hr_vol=vol24, include_24hr_change=change24)

    if only_price is True:
        return ticker_data[ticker][currency]
    else:
        price = ticker_data[ticker][currency]
        try:
            vol = round(ticker_data[ticker][currency + '_24h_vol'], 2)
            change = round(ticker_data[ticker][currency + '_24h_change'], 2)
        except:
            vol = 0
            change = 0
        return price, vol, change
