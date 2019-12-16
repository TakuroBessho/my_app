import _importpath
import sqlite3
import datetime
import api.coingecko
from api import get_stock_price as sp
import api.get_fx_rate
from api import sharedata as sd

# 一日ごとに金融商品の価格をデータベースに格納するための実行ファイル

# データベースのパスを指定
dbpath = api.sharedata.get_db_path()

# データベースに接続する
c = sqlite3.connect(dbpath)
cur = c.cursor()

# 今日の時刻を取得する
now = datetime.datetime.now()

# 各通貨のIDを取得
tickers = sd.get_tickers()
gold_id, n225_day_id, djia_day_id, world_index_id = tickers[
    6], tickers[10], tickers[11], tickers[7]


# FREDとヤフーファイナンスから日経平均とダウと金と上場インデックス世界株式(MSCI ACWI)
# の価格を取得する
n225_date = sp.pd_lastday_price_from_fred('NIKKEI225')[0]
n225_price = sp.pd_lastday_price_from_fred('NIKKEI225')[1]
djia_date = sp.pd_lastday_price_from_fred('DJIA')[0]
djia_price = sp.pd_lastday_price_from_fred('DJIA')[1]
gold_price = sp.get_gold_price()
world_index_price = sp.get_worldindex_price()


# クエリの作成,出来高の部分はとりあえず0、もし取れそうならコードを追加する
n225days_exe = f"'{n225_date}','{n225_day_id}','{n225_price}','{0}'"
djia_exe = f"'{djia_date}','{djia_day_id}','{djia_price}','{0}'"
gold_exe = f"'{now}','{gold_id}','{gold_price}','{0}'"
world_index_exe = f"'{now}','{world_index_id}','{world_index_price}','{0}'"


sql_n225days = f'insert into price_data(date,id,price,vol) VALUES ({n225days_exe});'
sql_djia = f'insert into price_data(date,id,price,vol) VALUES ({djia_exe});'
sql_gold = f'insert into price_data(date,id,price,vol) VALUES ({gold_exe});'
sql_world_index = f'insert into price_data(date,id,price,vol) VALUES ({world_index_exe});'


# クエリを実行する
cur.execute(sql_n225days)
cur.execute(sql_djia)
cur.execute(sql_gold)
cur.execute(sql_world_index)

# 保存する（忘れると保存されないので注意）
c.commit()

# データベースとの接続を終了する
c.close()
