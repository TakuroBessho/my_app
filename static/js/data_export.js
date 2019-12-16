var start_array = [];
var end_array = [];


// 文字列を日時型に変換する関数
function toDate(str, delim) {
    var arr = str.split(delim)
    return new Date(arr[0], arr[1] - 1, arr[2]);
};


// JSで取得した現在時間をインポート画面の表示形式に変換する関数
function get_now() {
    var now = new Date();
    var Year = now.getFullYear();
    var Month = now.getMonth() + 1;
    var Date2 = now.getDate();
    var Hour = now.getHours();
    var Min = now.getMinutes();
    var Sec = now.getSeconds();

    return Year + "/" + Month + "/" + Date2 + "/" + Hour + ":" + Min + ":" + Sec;
};


// date-pickerでカレンダーを表示する関数
$('#date_sample').datepicker({
    orientation: 'bottom',
    language: 'ja',
});

$('#date_sample2').datepicker({
    orientation: 'bottom',
    language: 'ja',
});

// エクスポートボタンがクリックされたときの処理
$('#export_btn').on('click', function (event) {

    // 通常のsubmitアクションをキャンセルする
    event.preventDefault();


    var $form = $('#export_form');
    var query = $form.serializeArray();
    var flag = 0;
    var form2 = document.forms.export;
    var start_date = toDate(form2.start.value, '/');
    var end_date = toDate(form2.end.value, '/');
    var export_term = $('#export_term')[0].value

    // 入力必須項目が入力されているかチェック、不適切な場合は各エラーコードとそれに対応したエラーメッセージを返す

    //入力フォームに空欄がある場合はエラーログ1を返す
    if (document.export.start.value == "" || document.export.end.value == "") {
        flag = 1;
    }
    //入力日時が出力日時よりもあとならばエラー2を返す
    else if (end_date.getTime() < start_date.getTime()) {
        flag = 2;
    }
    //入力日時と出力日時がexport_term日以上離れている場合はエラーログ3を返す
    else if (((end_date.getTime() - start_date.getTime()) / 86400000) >= export_term) {
        flag = 3;
    }



    // 入力必須項目に未入力があった場合
    if (flag == 1) {
        $('#danger_message').html("");
        $("#toast_message")[0].innerText = 'エクスポート対象期間を指定してください。';
        $("#toast_learning_start").toast("show");
        return false; // 送信中止
    }
    // 開始日が終了日よりも後日だった場合
    else if (flag == 2) {
        $('#danger_message').html("");
        $("#toast_message")[0].innerText = 'エクスポート期間の指定が不適切です。もう一度確認してください';
        $("#toast_learning_start").toast("show");
        return false; // 送信中止
    }
    // 開始日と終了日の差がexport_termの設定日以上の長さだった場合
    else if (flag == 3) {
        $('#danger_message').html("");
        $("#toast_message")[0].innerText = 'エクスポート期間は' + String(export_term) + '日以内で指定してください';

        return false; // 送信中止

        // 入力必須項目が全て入力済みだった場合AJAXで送信する
    } else {

        // 開始日と終了日の組み合わせをチェックリストから検索し既に同じものがあればキャンセル
        start_cheak = start_array.some(item => item === form2.start.value)
        end_cheak = end_array.some(item => item === form2.end.value)

        if (start_cheak == true && end_cheak == true) {
            // すでに同じ指定期間のデータが作成されていた場合トーストメッセージを表示
            $('#danger_message').html("");
            $("#toast_message")[0].innerText = 'すでに同じ期間のZIPファイルが作成されています';
            $("#toast_learning_start").toast("show");
            return false; // 送信中止
        }

        // 無ければチェックリストに要素を追加
        start_array.push(form2.start.value);
        end_array.push(form2.end.value);

        //処理中・・・のテキストを作成する
        var element = document.createElement('div');

        element.id = "processing";
        element.classList.add("alert", "alert-warning");
        element.style.fontSize = "90%";
        element.innerHTML = '<img src="static/img/exe_loading.gif" width="20" height="20"></img> ' + ' [' + get_now() + '] ' + form2.start.value + '~' + form2.end.value + 'エクスポートを開始しました。';
        document.getElementById("result_area").appendChild(element);


        // AJAX通信開始
        $.ajax({
            url: '/export_csv', // Formのアクションを取得して指定する
            type: 'get', // Formのメソッドを取得して指定する
            data: query, // データにFormがserialzeした結果を入れる
        }).done(function (response) {
            // 開始日と終了日のデータを配列から削除する
            start_array = start_array.filter(n => n !== form2.start.value);
            end_array = end_array.filter(n => n !== form2.end.value);

            if (response == 'empty') {
                // エクスポートを開始しました・・・を削除する
                $("#processing").remove();
                // 指定期間のデータが0件の場合トーストメッセージを表示 
                $('#danger_message').html("");
                $("#toast_message")[0].innerText = '指定された期間のデータが0件です';
                $("#toast_learning_start").toast("show");
            } else if (response == 'make_failure') {
                // エクスポートを開始しました・・・を削除する
                $("#processing").remove();
                // すでに同じ指定期間のデータが作成されていた場合トーストメッセージを表示
                $('#danger_message').html("");
                $("#toast_message")[0].innerText = 'すでに同じ期間のZIPファイルが作成されています';
                $("#toast_learning_start").toast("show");
            } else if (response == 'unexpected_error') {
                // エクスポートを開始しました・・・を削除する
                $("#processing").remove();
                // サーバー側で予期せぬエラーが発生した場合トーストメッセージを表示
                $('#danger_message').html("");
                $("#toast_message")[0].innerText = '予期せぬエラーが発生しました。サーバー側に問い合わせてください';
                $("#toast_learning_start").toast("show");
            } else {
                // エクスポートを開始しました・・・を削除する
                $("#processing").remove();
                // エクスポートが成功した場合はダウンロードリンクにアクセスしてダウンロードを開始する
                window.location.href = "/export_action/" + response
                console.log(response)
            };
        }).fail(function () {})
    }
});