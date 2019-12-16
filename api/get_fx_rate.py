from bs4 import BeautifulSoup
import urllib.request as req


def get_rate_jpyusd():
    """[日本円とドルの為替レートを取得する関数]
    スクレイピングに異常が発生した場合はとりあえず105を返す
    Returns:
        [float] -- [日本円とドルのレート]
    """
    try:
        url = "https://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
        res = req.urlopen(url)
        soup = BeautifulSoup(res, 'html.parser')
        d1 = soup.select_one(".stoksPrice").string
        return round(float(d1), 3)
    except:
        return 105
