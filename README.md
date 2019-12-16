<h1>暗号通貨と株式の価格データベースサイト</h1>
<p> </p>
<h3>開発環境</h3>
<p><strong>・Python3.4(Flask)</strong></p>
<p><strong>・Linux(Centos7)</strong></p>
<p><strong>・Appache</strong></p>
<p><strong>・wsgi</strong></p>
<p><strong>・bootstrap</strong></p>
<p><strong>・Vscode</strong></p>
<p> </p>
<p> </p>
<h3>アプリの画面機能一覧</h3>
<p><strong>・トップページ(/)</strong></p>
<p><strong>・各通貨の直近の価格チャートとテクニカル指標(/indicator)</strong></p>
<p><strong>・csvエクスポート機能(/data_export)</strong></p>
<p><strong>・ログイン機能(/signin)</strong></p>
<p><strong>・新規登録画面(/signup)</strong></p>
<p><strong>・自動取引BOTの成績表示画面(/trade_performance)</strong></p>
<p> </p>
<h3>MVC構成</h3>
<p><strong>・app_run.py --- コントローラー部分</strong></p>
<p><strong>・db/crypto.sqlite --- データベース(Model)</strong></p>
<p><strong>・templates/ --- pcからアクセスしたときに表示されるVIEW</strong></p>
<p><strong>・templates/mobile --- スマホ・タブレットからアクセスしたときに表示されるVIEW</strong></p>
<p> </p>
<p> </p>
<h3>その他ファイル構成</h3>
<p> </p>
<h4><strong>・/api </strong></h4>
<p><strong>ファイルパスやデータの取得に使用するAPI関連の関数を記述したファイル用のディレクトリ</strong></p>
<p> </p>
<p> </p>
<p><strong> coingecko.py --- 暗号通貨の価格を取得する処理を関数化してまとめたファイル</strong></p>
<p><br /><strong> common.py --- メール処理などの汎用的な処理を記述(予定)のファイル</strong></p>
<p><br /><strong> get_fx_rate.py --- 為替レートのAPI処理を記述したファイル</strong></p>
<p><br /><strong> get_stock_price.py --- 株価データを取得するAPI関連の処理をまとめたファイル</strong></p>
<p><br /><strong> sharedata.py --- API鍵や初期設定パスを記述したファイル</strong></p>
<p><br /><strong> twitter_oauth.py　--- Oauth認証の処理を記述した関数をまとめたファイル</strong></p>
<p> </p>
<p> </p>
<h4>・/db</h4>
<p><strong>データベースを操作する系のファイルのディレクトリ</strong></p>
<p><br /> <strong>db_to_pricedata.py --- APIで取得した価格データを一定時間ごとにDBに保存する処理を行うファイル(cronで5分おきに定期実行)</strong></p>
<p><br /><strong> db_to_stockdata.py --- 一日ごとに日経平均とダウの株価データを取得する関数(cronで一日おきに定期実行)</strong></p>
<p><br /><strong>manipulate_db.py --- データベースを操作する関数をまとめたファイル(クラスで呼び出す)</strong></p>
<p> </p>
<p> </p>
<h4>・/export_tmp</h4>
<p>出力したcsvを置いておくファイル</p>
<p> </p>
<p> </p>
<p> </p>
<p>とりあえずフロント部分の見栄えをもっとモダンにしたいので、そのあたりを中心にアドバイスいただけると嬉しいです。</p>
<p> </p>
<p> </p>
<p> </p>