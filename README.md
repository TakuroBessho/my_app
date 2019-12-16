<h1 dir="auto">暗号通貨と株式の価格データベースサイト</h1>
<p dir="auto"> </p>
<h3 dir="auto"><a id="user-content-開発環境" class="anchor" href="#%E9%96%8B%E7%99%BA%E7%92%B0%E5%A2%83" aria-hidden="true"> </a>開発環境</h3>
<p dir="auto"><strong>・Python3.4(Flask)</strong></p>
<p dir="auto"><strong>・Linux(Centos7)</strong></p>
<p dir="auto"><strong>・Appache</strong></p>
<p dir="auto"><strong>・wsgi</strong></p>
<p dir="auto"><strong>・bootstrap</strong></p>
<p dir="auto"><strong>・jquery</strong></p>
<p dir="auto"><strong>・Vscode</strong></p>
<p dir="auto"> </p>
<p dir="auto"> </p>
<h3 dir="auto"><a id="user-content-アプリの画面機能一覧" class="anchor" href="#%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AE%E7%94%BB%E9%9D%A2%E6%A9%9F%E8%83%BD%E4%B8%80%E8%A6%A7" aria-hidden="true"> </a>アプリの画面機能一覧</h3>
<p dir="auto"><strong>・トップページ(/)</strong></p>
<p dir="auto"><strong>・各通貨の直近の価格チャートとテクニカル指標(/indicator)</strong></p>
<p dir="auto"><strong>・csvエクスポート機能(/data_export)</strong></p>
<p dir="auto"><strong>・※ログイン機能(/signin)</strong></p>
<p dir="auto"><strong>・新規登録画面(/signup)</strong></p>
<p dir="auto"><strong>・自動取引BOTの成績表示画面(/trade_performance)</strong></p>
<p dir="auto"> </p>
<p dir="auto">※ソーシャルログインのみ</p>
<p dir="auto"> </p>
<h3 dir="auto"><a id="user-content-mvc構成" class="anchor" href="#mvc%E6%A7%8B%E6%88%90" aria-hidden="true"> </a>MVC構成</h3>
<p dir="auto"><strong>・app_run.py --- コントローラー部分</strong></p>
<p dir="auto"><strong>・db/crypto.sqlite --- データベース(Model)</strong></p>
<p dir="auto"><strong>・templates/ --- pcからアクセスしたときに表示されるVIEW</strong></p>
<p dir="auto"><strong>・templates/mobile --- スマホ・タブレットからアクセスしたときに表示されるVIEW</strong></p>
<p dir="auto"> </p>
<p dir="auto"> </p>
<h3 dir="auto"><a id="user-content-その他ファイル構成" class="anchor" href="#%E3%81%9D%E3%81%AE%E4%BB%96%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E6%A7%8B%E6%88%90" aria-hidden="true"> </a>その他ファイル構成</h3>
<p dir="auto"> </p>
<h4 dir="auto"><a id="user-content-api" class="anchor" href="#api" aria-hidden="true"> </a><strong>・/api </strong></h4>
<p dir="auto"><strong>ファイルパスやデータの取得に使用するAPI関連の関数を記述したファイル用のディレクトリ</strong></p>
<p dir="auto"> </p>
<p dir="auto"> </p>
<p dir="auto"><strong> coingecko.py --- 暗号通貨の価格を取得する処理を関数化してまとめたファイル</strong></p>
<p dir="auto"><br /><strong> common.py --- メール処理などの汎用的な処理を記述(予定)のファイル</strong></p>
<p dir="auto"><br /><strong> get_fx_rate.py --- 為替レートのAPI処理を記述したファイル</strong></p>
<p dir="auto"><br /><strong> get_stock_price.py --- 株価データを取得するAPI関連の処理をまとめたファイル</strong></p>
<p dir="auto"><br /><strong> sharedata.py --- API鍵や初期設定パスを記述したファイル</strong></p>
<p dir="auto"><br /><strong> twitter_oauth.py　--- Oauth認証の処理を記述した関数をまとめたファイル</strong></p>
<p dir="auto"> </p>
<p dir="auto"> </p>
<h4 dir="auto"><a id="user-content-db" class="anchor" href="#db" aria-hidden="true"> </a>・/db</h4>
<p dir="auto"><strong>データベースを操作する系のファイルのディレクトリ</strong></p>
<p dir="auto"><br /> <strong>db_to_pricedata.py --- APIで取得した価格データを一定時間ごとにDBに保存する処理を行うファイル(cronで5分おきに定期実行)</strong></p>
<p dir="auto"><br /><strong> db_to_stockdata.py --- 一日ごとに日経平均とダウの株価データを取得する関数(cronで一日おきに定期実行)</strong></p>
<p dir="auto"><br /><strong>manipulate_db.py --- データベースを操作する関数をまとめたファイル(クラスで呼び出す)</strong></p>
<p dir="auto"> </p>
<p dir="auto"> </p>
<h4 dir="auto"><a id="user-content-export_tmp" class="anchor" href="#export_tmp" aria-hidden="true"> </a>・/export_tmp</h4>
<p dir="auto">出力したcsvを置いておくファイル</p>
