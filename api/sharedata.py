

# tickerid & tickername
tickers_dict = {
    'btc': 1, 'btcfx': 2, "bsv": 3, 'xrp': 4, 'NIKKEI225': 5,
    'DJIA': 6, 'gold': 7, 'world_index': 8, 'eth': 9, 'jpy_usd': 10,
    'N225_day': 11, 'DJIA_day': 12, 'bnb': 13, 'tpay': 14
}


tickers_dict2 = {
    'btc': 'Bitcoin', 'btcfx': 'BTC_FX', "bsv": 'BitcoinSV', 'xrp': 'Ripple', 'NIKKEI225': '日経平均',
    'DJIA': 'ダウ平均株価', 'gold': 'Gold', 'world_index': '世界株式インデックス', 'eth': 'Ethereum', 'jpy_usd': 'ドル円',
    'N225_day': '日経平均', 'DJIA_day': 'ダウ平均株価', 'bnb': 'Binance-Coin', 'tpay': 'Tokenpay'
}

# ファイル出力の際に仕様(開発環境と本番環境でPATHを変更する必要あり)
#base_path = 'C:\\Users\\81903\\Documents\\GitHub\\pricedata-analysis.com'
base_path = 'C:\\Users\\81903\\Desktop\\webapp_withflask-master'
# 本番環境のPATH
#base_path = '/var/www/html/app'


def get_twitter_apikey():
    # twitter api key for pricedata tweet  with crypto_analysis
    consumer_key = ''
    consumer_secret = ''
    access_key = 'i'
    access_secret = ''
    return consumer_key, consumer_secret, access_key, access_secret


def get_tweet_apikey():
    # twitter api key for pricedata tweet  with crypto_analysis
    consumer_key = ''
    consumer_secret = ''
    access_key = 'i'
    access_secret = ''
    return consumer_key, consumer_secret, access_key, access_secret


# database file path
def get_db_path():
    """[データベースのPATHを返す関数]
        テスト環境と本番環境のPATHはここを切り替えて管理する
    Returns:
        [str] -- [データベースのPATH]
    """

    # データベースのパスを指定
    #dbpath = 'C:\\Users\\81903\\Documents\\GitHub\\pricedata-analysis.com\\db\\crypto.sqlite'
    dbpath = 'C:\\Users\\81903\\Desktop\\webapp_withflask-master\\db\\crypto.sqlite'
    # 本番環境のPATH
    #dbpath = '/var/www/html/app/db/crypto.sqlite'
    return dbpath


def get_tickers():
    btc_id = 1
    btcfx_id = 2
    bsv_id = 3
    xrp_id = 4
    NIKKEI225 = 5
    DJIA = 6
    gold = 7
    world_index = 8
    eth_id = 9
    jpy_usd = 10
    N225_day = 11
    DJIA_day = 12
    bnb = 13
    tpay = 14
    return btc_id, btcfx_id, bsv_id, xrp_id, +\
        NIKKEI225, DJIA, gold, world_index, eth_id, +\
        jpy_usd, N225_day, DJIA_day, bnb, tpay
