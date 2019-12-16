
import _importpath
import sqlite3
import pandas as pd
from api import sharedata
from pathlib import Path
import shutil

# get stockprice from my DB
tickers_id = sharedata.tickers_dict
tickers_name = sharedata.tickers_dict2


class DB:
    def __init__(self):
        # connect database
        self.dbpath = sharedata.get_db_path()
        self.c = sqlite3.connect(self.dbpath, check_same_thread=False)
        self.cur = self.c.cursor()

    def select_price_data(self, id_, limit):
        """[価格データテーブルから任意の通貨のデータを引っ張ってくる関数]]
        id_ : int
            通貨のID
        limit : int
            取得したい行数
        """

        self.__init__()
        quary = 'select * from price_data where id=' + \
            str(id_) + ' order by date DESC limit ' + str(limit)

        self.cur.execute(quary)
        list_ = self.cur.fetchall()
        names = list(map(lambda x: x[0], self.cur.description))
        df = pd.DataFrame(list_, columns=names)
        self.c.close()
        return df

    def calc_trade_performance(self, new_query, bot_num, limit):
        """[トレードパフォーマンスを計算する関数]
            テーブルにデータがない場合、エラーで失敗する可能性高し
        Arguments:
            new_query {[tuple]} -- [BOTの取引データをタプルにしたもの]]
            bot_num {[INT]} -- [botの番号]
            limit {[int]} -- [テーブルから引っ張るデータの上限数]

        Returns:
            [tuple]] -- [各トレード利益の計算結果]
        """

        self.__init__()
        quary = 'select * from trade_performance where bot_num=' + \
            str(bot_num) + ' order by date DESC limit ' + str(limit)
        self.cur.execute(quary)
        list_ = self.cur.fetchall()
        # 前回の残高を取得する
        last_balance = list_[0][3]
        # 今回の残高
        new_balance = new_query[3]
        # 前回と今回の変化率を計算する
        profit = (new_balance - last_balance) / last_balance * 100
        profit_money = new_balance - last_balance
        # 累積変化率を計算する（今後追加予定とりあえずは0で埋めておく）
        total_profit = 0
        return profit, total_profit, profit_money

    def bot_insert_db(self, query):
        """[botの記録をテーブルにINSERTする関数]

        Arguments:
            query {[tuple]}
            -- [テーブルにINSERTするためのBOTのデータがタプルで格納されている]
        """
        bot_num = query[1]
        limit = 3
        try:
            profit, total_profit, profit_money = self.calc_trade_performance(
                query, bot_num, limit)
        except Exception as e:
            print('insertdb', e.args)
            profit, total_profit, profit_money = 0, 0, 23000
        insert_query = f"'{query[0]}','{query[1]}','{query[2]}','{query[3]}', '{query[4]}', '{profit}', '{total_profit}', '{profit_money}'"
        sql = 'insert into trade_performance(date,bot_num,exchange,balance,order_type,profit,total_profit,profit_money) VALUES (' + insert_query + ');'
        self.cur.execute(sql)
        self.c.commit()
        self.c.close()

    def get_bot_performance(self, bot_num, limit):
        """[botのパフォーマンスデータを抽出する関数]

        Arguments:
            bot_num {[int]} -- [botの番号]
            limit {[int]}} -- [呼び出すクエリ数]

        Returns:
            [df] -- [データフレーム]
        """

        self.__init__()
        quary = 'select * from trade_performance where bot_num=' + \
            str(bot_num) + ' order by date DESC limit ' + str(limit)
        self.cur.execute(quary)
        list_ = self.cur.fetchall()
        return list_

    def get_latest_cryptodata(self, id_):
        """[データベースの最新の暗号通貨価格と変化率を返す関数]

        Arguments:
            id_ {[int]} -- [各通貨のID]
        Returns:
            [TUPLE] -- [価格と変化率のTUPLE]]
        """
        data = self.select_price_data(id_, 2)
        price = data['price'].values[0]
        change24 = data['change24'].values[0]
        return price, change24

    def get_latest_stockdata(self, id_):
        """[データベースの最新の金融商品価格と変化率を返す関数]

        Arguments:
            id_ {[int]} -- [各通貨のID]
        Returns:
            [TUPLE] -- [価格と変化率のTUPLE]]
        """

        try:
            data = self.select_price_data(id_, 2)
            price = data['price'].values[0]
            pre_price = data['price'].values[1]
            change24 = round((price - pre_price) / pre_price * 100, 2)
            return price, change24
        except:
            price, change24 = 0, 0
            return price, change24


    def get_datalength(self, _id):
        """[データの長さを返す関数]

        Arguments:
            _id {[int]} -- [通貨のID、SharedataのDICTを参照]

        Returns:
            [type] -- [description]
        """

        self.__init__()
        quary = 'select count(price) from price_data where id=' + str(_id)
        self.cur.execute(quary)
        length = self.cur.fetchall()[0][0]
        return length

    def search_user(self, access_token):
        """[アクセストークンからユーザー情報を検索して一致するものがあればTrue
        なければFalseを返す関数]

        Returns:
            [dict] -- [辞書型のアクセストークン]

        Returns:
            [type] -- [description]
        """

        self.__init__()
        user_token = access_token['oauth_token']
        user_secret = access_token['oauth_token_secret']
        user_id = access_token['user_id']

        query = "select * from user_info where user_token=" + "'" + user_token + "'" + " and" + \
            ' user_secret=' + "'" + user_secret + "'" + " and" + ' user_id=' + user_id

        self.cur.execute(query)
        user_data = self.cur.fetchall()
        print(user_data)
        self.c.close()

        if user_data == []:
            return False
        else:
            return user_data[0]

    def register_userinfo(self, access_token):
        """[アクセストークンから取得したユーザー情報をテーブルにINSERTする関数]

        Returns:
            [dict] -- [辞書型のアクセストークン]

        Returns:
            [type] -- [description]
        """

        user_oauth_token = access_token['oauth_token']
        user_oauth_token_secret = access_token['oauth_token_secret']
        user_id = int(access_token['user_id'])
        user_screen_name = access_token['screen_name']
        provider = 'twitter'

        self.__init__()
        insert_query = f"'{user_id}','{user_screen_name}','{provider}','{user_oauth_token}', '{user_oauth_token_secret}'"
        sql = 'insert into user_info(user_id,user_screen,provider,user_token,user_secret) VALUES (' + \
            insert_query + ');'
        self.cur.execute(sql)
        self.c.commit()
        self.c.close()

    def get_dashboard(self):
        """[ダッシュボード用の価格を取得する関数]
        Returns [tuple]
        """
        btc = self.get_latest_cryptodata(tickers_id['btc'])
        eth = self.get_latest_cryptodata(tickers_id['eth'])
        xrp = self.get_latest_cryptodata(tickers_id['xrp'])
        bsv = self.get_latest_cryptodata(tickers_id['bsv'])
        bnb = self.get_latest_cryptodata(tickers_id['bnb'])
        tpay = self.get_latest_cryptodata(tickers_id['tpay'])
        gold = self.get_latest_stockdata(tickers_id['gold'])
        n225 = self.get_latest_stockdata(tickers_id['NIKKEI225'])
        djia = self.get_latest_stockdata(tickers_id['DJIA'])
        vt = self.get_latest_stockdata(tickers_id['world_index'])
        return btc, eth, xrp, bsv, bnb, tpay, gold, n225, djia, vt

    def create_api_dict(self, terms):
        if terms == '5min':
            btc, eth, xrp, bsv, bnb, tpay, gold, n225, djia, vt = self.get_dashboard()
            price_data = {
                'BTC': btc[0],
                'BTCchange': btc[1],
                'ETH': eth[0],
                'ETHchange': eth[1],
                'XRP': xrp[0],
                'XRPchange': xrp[1],
                'BSV': bsv[0],
                'BSVchange': bsv[1],
                'BNB': bnb[0],
                'BNBchange': bnb[1],
                'TPAY': tpay[0],
                'TPAYchange': tpay[1],
            }
        elif terms == '60min':
            price_data = []
        elif terms == '1day':
            price_data = []
        else:
            price_data = []

        return price_data

    def data_export(self, id_, start, end, pattern):
        """[データベースから価格データをcsvにexportする関数]

        Arguments:
            id_ {[int]} -- [各金融商品のティッカーID]
            start {[datetime]} -- [開始日]
            end {[datetime]} -- [終了日]
            pattern {[int]} -- [エクスポート形式]

        Returns:
            [file_path] -- [出力するファイル名とパス]
        """
        # 日付の形式を整える
        self.__init__()
        base_path = Path(sharedata.base_path)
        export_path = base_path/'export_tmp'
        start = start.replace('/', '-')
        end = end.replace('/', '-')
        # データベースからデータを引っ張ってきてデータフレームにする
        quary = f"select * from price_data where date < '{end}' and date > '{start}' and id={id_}"
        self.cur.execute(quary)
        list_ = self.cur.fetchall()
        names = list(map(lambda x: x[0], self.cur.description))
        df = pd.DataFrame(list_, columns=names)
        df = df.drop(["id", "change24"], axis=1)
        # データフレームをcsvに出力する
        file_name = f'{start}-{end}.csv'
        df.to_csv(str(export_path/file_name), index=False, mode='w')
        # 出力したcsvを移動する
        #shutil.move(f'{base_path}/{file_name}', f'{export_path}/{file_name}')
        return file_name

# DB = DB()
# df = DB.get_datalength(1)
# print(df)
