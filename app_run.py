import _importpath
from flask import Flask, render_template, request, redirect, session, url_for
from flask import jsonify, send_from_directory
import flask_devices
import talib as ta
from pathlib import Path

# my library
from models import manipulate_db
from api import sharedata, twitter_oauth as to

# init_application
app = Flask(__name__)

devices = flask_devices.Devices(app)
devices.add_pattern('mobile', 'iPhone|iPod|Android.*Mobile|Windows.*Phone|dream|blackberry|CUPCAKE|webOS|incognito|webmate', 'C:\\Users\\81903\\Desktop\\webapp_withflask-master\\templates\\mobile')
devices.add_pattern('tablet', 'iPad|Android', 'C:\\Users\\81903\\Desktop\\webapp_withflask-master\\templates')
devices.add_pattern('pc', '.*', 'C:\\Users\\81903\\Desktop\\webapp_withflask-master\\templates')

db = manipulate_db.DB()

# get stockprice from my DB
tickers_id = sharedata.tickers_dict
tickers_name = sharedata.tickers_dict2

# セッションの暗号化のための文字列(適当でOK)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# view_crypto_index
@app.route("/")
def crypto_index():
    """[ホーム画面]

    Returns:
        [htmlとテンプレート変数] -- [各通貨の価格と24時間変化率]
    """

    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []
    print(request.DEVICE)
    # get crypto price with coingecko API
    btc, eth, xrp, bsv, bnb, tpay, gold, n225, djia, vt = db.get_dashboard()

    # スマホからのアクセスとPC・タブレットのアクセスで表示画面を切り替える
    if request.DEVICE == 'mobile':
        return render_template(
            'mobile_index_dashbord.html', user_name=user_name, btc=btc[0], btc24=btc[1],
            eth=eth[0], eth24=eth[1], xrp=xrp[0], xrp24=xrp[1], bsv=bsv[0], bsv24=bsv[1],
            bnb=bnb[0], bnb24=bnb[1], tpay=tpay[0], tpay24=tpay[1], djia=djia[0], djia24=djia[1], N225=n225[0], N22524=n225[1],
            gold=gold[0], gold24=gold[1], vt=vt[0], vt24=vt[1])

    else:
        return render_template(
            'crypto_dashbord.html', user_name=user_name, btc=btc[0], btc24=btc[1],
            eth=eth[0], eth24=eth[1], xrp=xrp[0], xrp24=xrp[1], bsv=bsv[0], bsv24=bsv[1],
            bnb=bnb[0], bnb24=bnb[1], tpay=tpay[0], tpay24=tpay[1], djia=djia[0], djia24=djia[1], N225=n225[0], N22524=n225[1],
            gold=gold[0], gold24=gold[1], vt=vt[0], vt24=vt[1])


# plot_technical indicator
@app.route("/indicator_<ticker>_<terms>")
def indicator_crypto(ticker, terms):
    """[テクニカル指標を計算する関数（ここで計算するかあらかじめ
        内部で計算した数値を返すか検討中、とりあえずはここで計算して返す仕様でいく）]
    Arguments:
        ticker {[str]} -- [sharedataに記載している各コイン・株式のTICKER]

    Returns:
        [html] -- [htmlとJINJA2用の関数を返す]
    """

    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []

    # get ticker and pricedata
    id_ = tickers_id[ticker]
    ticker_ = tickers_name[ticker]
    pricedata = db.select_price_data(id_, 36)

    # sort pricedata with pandas
    pricedata = pricedata.sort_values('date')
    calc_data = pricedata['price'].values
    price_list = pricedata['price'].to_list()[-16:]
    price_index = pricedata['date'].to_list()[-16:]

    # calc EMA
    sma_short = ta.SMA(calc_data, timeperiod=5)[-16:].tolist()
    sma_long = ta.SMA(calc_data, timeperiod=15)[-16:].tolist()
    # calc rsi
    rsi = ta.RSI(calc_data)[-16:].tolist()
    last_rsi = round(rsi[-1], 2)
    # calc_macd
    macd = ta.MACD(calc_data, fastperiod=5, slowperiod=15,
                   signalperiod=5)[2][-16:].tolist()
    last_macd = round(macd[-1], 2)
    # calc_momentam
    mom = ta.MOM(calc_data, timeperiod=5)[-16:].tolist()
    last_mom = round(mom[-1], 2)

    return render_template('crypto_indicater.html', user_name=user_name, ticker_=ticker_,
                           pricedata=price_list, plot_index=price_index,
                           sma_short=sma_short, sma_long=sma_long, macd=macd,
                           last_macd=last_macd, rsi=rsi, last_rsi=last_rsi,
                           mom=mom, last_mom=last_mom)


@app.route("/indicators_<ticker>")
def indicator_stock(ticker):
    """[株価系データの日足データを返す関数]

    Arguments:
        ticker {[str]} -- [ticker-NIKKEI225,DJIA etc...]]

    Returns:
        [html] -- [stock_indicater.html]
    """

    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []

    # get ticker and pricedata
    id_ = tickers_id[ticker]
    ticker_ = tickers_name[ticker]
    pricedata = db.select_price_data(id_, 30)

    # sort pricedata with pandas
    pricedata = pricedata.sort_values('date')
    calc_data = pricedata['price'].values
    price_list = pricedata['price'].to_list()[-16:]
    price_index = pricedata['date'].to_list()[-16:]

    # calc EMA
    sma_short = ta.SMA(calc_data, timeperiod=5)[-16:].tolist()
    sma_long = ta.SMA(calc_data, timeperiod=15)[-16:].tolist()
    # calc rsi
    rsi = ta.RSI(calc_data)[-16:].tolist()
    last_rsi = round(rsi[-1], 2)
    # calc_macd
    macd = ta.MACD(calc_data, fastperiod=5, slowperiod=15,
                   signalperiod=5)[2][-16:].tolist()
    last_macd = round(macd[-1], 2)
    # calc_momentam
    mom = ta.MOM(calc_data, timeperiod=5)[-16:].tolist()
    last_mom = round(mom[-1], 2)

    return render_template('stock_indicater.html', user_name=user_name, ticker_=ticker_,
                           pricedata=price_list, plot_index=price_index,
                           sma_short=sma_short, sma_long=sma_long, macd=macd,
                           last_macd=last_macd, rsi=rsi, last_rsi=last_rsi,
                           mom=mom, last_mom=last_mom)


@app.route("/trade_performance")
def view_auto_trade():
    """[自動取引BOTの成績を表示する関数]

    Returns:
        [html] -- [algorithmic_trade.html]
    """

    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []

    # get performancedata
    trade_data1 = [i for i in reversed(db.get_bot_performance(1, 7))]
    plot_index1 = [i[0][5:10] for i in trade_data1]
    plot_tradedata1 = [i[3] for i in trade_data1]
    # get last positon
    today_position = trade_data1[0][4]
    # trancerate japanese
    if today_position == 'sell':
        today_position = 'ショート(売り)'
    elif today_position == 'buy':
        today_position = 'ロング(買い)'
    else:
        today_position = 'ノーポジ'
    return render_template('algorithmic_trade.html', user_name=user_name,
                           exchange1=trade_data1[0][2],
                           today_position=today_position,
                           tradedata1=plot_tradedata1,
                           plot_index=plot_index1)


@app.route("/user_login")
def sign_in():
    """[ログイン画面を返す関数]

    Returns:
        [html] -- [signin.html]
    """
    return render_template("signin.html")


@app.route("/oauth_register")
def redirect_oauth():
    """[認証画面に遷移して内部でアクセストークンの登録などを行って
    　　からコールバックURLにリダイレクトする関数]

    Returns:
        [html] -- [callbackURL]
    """

    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = request.args.get('oauth_callback')
    # この関数でDBにアクセストークンとユーザー情報を登録している
    callback = to.get_twitter_request_token(oauth_callback)
    return redirect(callback)


@app.route('/callback')
def execute_userinfo():
    """[認証画面から返されてきた情報を取得して処理する関数]

    Returns:
        [html] [ホーム画面にリダイレクトする]
    """

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    # リクエストトークンからアクセストークンを取得
    access_token = to.get_twitter_access_token(oauth_token, oauth_verifier)

    # 既に登録していないかチェック、無ければ新規にデータをテーブルにINSERTする
    # 既に登録済みであれば、その情報を返す
    user_data = db.search_user(access_token)

    if user_data is False:
        # 新規ユーザーはアクセストークンの情報をデータベースに保存
        db.register_userinfo(access_token)
        # 登録してからもう一回ユーザーデータを取得
        user_data = db.search_user(access_token)

    # 返された情報をSessionに保存する
    session['user_name'] = access_token['screen_name']
    session['user_id'] = access_token['user_id']
    session['oauth_token'] = access_token['oauth_token']
    session['oauth_token_secret'] = access_token['oauth_token_secret']
    return redirect(url_for('crypto_index'))


# 未完成
@app.route("/get_accountdata")
def get_accountdata():
    """[認証したアカウントのデータを取得
    　　してツイートデータを表示する]

    Returns:
        [html] -- [rtest.html]
    """

    if session == []:
        return redirect(url_for('sign_in'))
    else:
        # アクセストークンからアカウントデータを取得する
        data = to.get_accountdata(
            session['user_id'],
            session['oauth_token'],
            session['oauth_token_secret']
        )
        return render_template("rtest.html", data=data)


@app.route("/user_register")
def sign_up():
    """[新規登録画面を返す関数]]
    
    Returns:
        [html] -- [signup.html]
    """
    return render_template("signup.html")


@app.route("/logout")
def logout():
    """[セッション情報を削除してログアウトする関数]

    Returns:
        [html] -- [ホーム画面にリダイレクト]
    """
    delete_data = ['user_name', 'user_id', 'oauth_token', 'oauth_secret']
    for data in delete_data:
        session.pop(data, None)
    return redirect(url_for('crypto_index'))


@app.route("/data_export")
def data_export():
    """[エクスポート画面を表示する関数]

    Returns:
        [html] -- [data_export.html]
    """

    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []
    export_term = 90
    return render_template(
        "data_export.html", export_term=export_term, user_name=user_name)


# まだ未完成！！！！
@app.route("/export_csv",  methods=["GET"])
def data_export_action():
    """[エクスポートするcsvを作成する関数]

    Returns:
        [String] -- [出力するCSVファイル名]
    """

    # html側からGETで送られてきた値を受け取る
    id_ = request.args['id_']
    start = request.args['start']
    end = request.args['end']
    value = request.args['choise_pattern']
    file_name = db.data_export(id_, start, end, value)
    return str(file_name)


# redirect download URL with ajax
@app.route("/export_action/<file_name>", methods=["GET"])
def export_action(file_name):
    """[ajax経由で貰ったcsvファイル名に一致するcsvファイルを出力する]

    Arguments:
        file_name {[String]} -- [csvファイル名(例：20191101-20191103.csv)]

    Returns:
        [?] -- [csvのダウンロード処理に必要な情報]
    """
    return send_from_directory(
        directory=str(Path(sharedata.base_path)/'export_tmp'),
        filename=file_name,
        as_attachment=True,
        attachment_filename=file_name,
        mimetype='XLSX_MIMETYPE')


@app.route("/api/<ticker>_<terms>", methods=["GET"])
def get_pricedata(ticker, terms):
    """[api的にJsonで価格データを返す関数]

    Arguments:
        ticker {[String]} -- [通貨名(例:bitcoin)]
        terms {[String]} -- [期間(例：5min)]

    Returns:
        [json] -- [Jsonで格納した各通貨の価格データ・出来高]
    """
    if ticker == 'all' and terms == '5min':
        price_data = db.create_api_dict('5min')
    else:
        # 個別の通貨ごとの設定
        pass
    return jsonify(price_data)


# 未完成
@app.route("/backtest_<bot_name>")
def calc_backtest(bot_name):
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []

    # get performancedata
    trade_data1 = [i for i in reversed(db.get_bot_performance(1, 7))]
    plot_index1 = [i[0][5:10] for i in trade_data1]
    plot_tradedata1 = [i[3] for i in trade_data1]
    # get last positon
    today_position = trade_data1[0][4]
    # trancerate japanese
    if today_position == 'sell':
        today_position = 'ショート(売り)'
    elif today_position == 'buy':
        today_position = 'ロング(買い)'
    else:
        today_position = 'ノーポジ'
    items = []
    for i in range(1, 11):
        i = str(i)

        # dict == {}
        # you just don't have to quote the keys
        an_item = dict(date="2012-02-" + i, id=i,
                       position="here", status="waiting")
        items.append(an_item)

    return render_template('backtest.html', user_name=user_name,
                           exchange1=trade_data1[0][2],
                           today_position=today_position,
                           tradedata1=plot_tradedata1,
                           plot_index=plot_index1, items=items)


if __name__ == "__main__":
    app.run(debug=True)
