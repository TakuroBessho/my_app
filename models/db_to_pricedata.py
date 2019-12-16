
import _importpath
import sqlite3
import datetime
from api import coingecko
from api import get_stock_price
from api import get_fx_rate
from api import sharedata

# --------注意事項--------
# リップルとビットコインの出来高は各通貨単位(XRP・BTC)
# 他の通貨は円ベースの出来高、ドルベースの出来高を欲しいときは為替レートを掛け合わせて算出する
# 日経とダウのAPIは死ぬかもしれないので代替手段を探しておく


# データベースのパスを指定
dbpath = sharedata.get_db_path()

# データベースに接続する
c = sqlite3.connect(dbpath)
cur = c.cursor()

# テーブルの作成(初回のみ)
try:
    # idとtickerのテーブルを作成する
    c.execute('create table crypto_id(id integer, ticker text)')

    # 時刻　価格　出来高を格納するテーブルを作成する
    c.execute(
        'create table price_data(date datetime, id integer, price float, vol float, change24 float)')

    # 自動取引BOTのパフォーマンス検証用テーブルの作成
    c.execute('create table trade_performance(date datetime, bot_num integer, exchange text, balance float, order_type text, profit float, total_profit float, profit_money float)')

    # 出来高の列を追加する
    # c.execute('alter table price_data add column vol float'

    # 24時間変化率の列を追加する
    # c.execute('alter table price_data add column change24 float')

except Exception as e:
    print(e)
    pass


# 今日の日付と時間(hour)を取得する
now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d %H:%M:00')

# TICKER一覧を取得する
ticker_dict = sharedata.tickers_dict

# 為替レートを取得
rate = get_fx_rate.get_rate_jpyusd()


ticker_list = [['bitcoin', ticker_dict['btc']],
               ['ethereum', ticker_dict['eth']],
               ['ripple', ticker_dict['xrp']],
               ['bitcoin-cash-sv', ticker_dict['bsv']],
               ['binancecoin',  ticker_dict['bnb']],
               ['tokenpay',  ticker_dict['tpay']]
               ]


for ticker in ticker_list:
    data = coingecko.get_lastprice(ticker[0], 'jpy', False)
    ticker_price = data[0]
    try:
        ticker_vol = data[1]
        ticker_change = data[2]
    except:
        ticker_vol = 0
        ticker_change = 0
    ticker_exe = f"'{date}','{ticker[1]}','{ticker_price}','{ticker_vol}','{ticker_change}'"
    sql_ticker = f'insert into price_data(date,id,price,vol, change24) VALUES ({ticker_exe});'
    cur.execute(sql_ticker)


# 日経平均とダウの価格を取得する&DBに保存する
nikkei = get_stock_price.get_nikkei225_now()
djia = get_stock_price.get_djia_now()

nikkei_exe = f"'{date}','{ ticker_dict['NIKKEI225']}','{nikkei}','{0}'"
djia_exe = f"'{date}','{ ticker_dict['DJIA']}','{djia}','{0}'"
rate_exe = f"'{date}','{ ticker_dict['jpy_usd']}','{rate}','{0}'"

sql_nikkei = f'insert into price_data(date,id,price,vol) VALUES ({nikkei_exe});'
sql_djia = f'insert into price_data(date,id,price,vol) VALUES ({djia_exe});'
sql_rate = f'insert into price_data(date,id,price,vol) VALUES ({rate_exe});'

cur.execute(sql_nikkei)
cur.execute(sql_djia)
cur.execute(sql_rate)


# 保存する（忘れると保存されないので注意）
c.commit()

# データベースとの接続を終了する
c.close()
