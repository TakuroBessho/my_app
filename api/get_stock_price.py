from datetime import datetime
from datetime import timedelta
import requests
import json
import pandas as pd
import pandas_datareader as web
from bs4 import BeautifulSoup
import urllib.request as req


def send_email():
    """[メールを送信する関数]
    """
    return


def get_worldindex_price():
    """[ヤフーファイナンスから上場インデックス世界株式(MSCI ACWI)の価格を取得する関数]
    スクレイピングに異常が発生した場合はとりあえずメール送信
    Returns:
        [float] -- [worldindexの価格]
    """
    try:
        url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=1554.T"
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'html.parser')
        d1 = soup.table.find_all("td")[1].string
        return round(int(d1.replace(',', '')), 2)
    except:
        # メール送信
        print('今日は閉場日です')
        pass


def get_gold_price():
    """[ヤフーファイナンスから金の先物価格を取得する関数]
    スクレイピングに異常が発生した場合はとりあえず105を返す
    Returns:
        [float] -- [金の先物価格]
    """
    try:
        url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=1328.T"
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'html.parser')
        d1 = soup.table.find_all("td")[1].string
        return d1.replace(',', '')

    except Exception as e:
        # メール送信
        print('今日は閉場日です')
        print('gold', e.args)
        pass


def get_nikkei225_now():
    r = requests.get(
        "https://api.matumo.com/kabu/kabu_ave_realtime_api_v1.php")
    nikkei = r.text.split(',')[4]
    return nikkei


def get_djia_now():
    r = requests.get(
        "https://api.matumo.com/kabu/kabu_ave_realtime_api_v1.php")
    dau = r.text.split(',')[7]
    return dau


def get_nikkei225_all(end, start='1950/04/01'):
    nikkei = web.DataReader('NIKKEI225', "fred", start, end)
    return nikkei


def pd_lastday_price_from_fred(ticker):
    """[fredから昨日の金融商品価格を取得する関数]
    parameter
        [ticker] -- [FRED内部のTICKER]
                    例)日経平均-NIKKEI225、ダウーDJIA
    Returns:
        [float] -- [今日の日経平均]
    """

    day = datetime.now().date() - timedelta(days=1)
    nikkei = web.DataReader(ticker, "fred", day)
    try:
        price = nikkei[ticker].values[0]
        date = nikkei.index[0]
        return date, price
    except:
        print('昨日は閉場日です')
