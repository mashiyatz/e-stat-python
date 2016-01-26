# 中間アプリ


## 概要
中間アプリはe-Stat APIを使いやすくするためのPythonライブラリです。

## 事前にインストールするライブラリ等
本ライブラリを使用する前に下記のライブラリ等は予めインストールしてください。

### Pythonライブラリ
	pandas,numpy,math,Flask


## ディレクトリ及びファイル構成
(ディレクトリがない場合は作成してください)

    ├ data-cache/	 				 キャッシュ用ディレクトリ(データがCSV形式で保存されます)  
    ├ dictionary/					 辞書用ディレクトリ(検索用の辞書が作成されます)  
    ├ python/						 Pythonライブラリ用ディレクトリ  
    │  └ e_STat_API_Adaptor.py    
    ├ tmp/						 一時ダウンロード用ディレクトリ(json形式の元データを一時的に保存します)  
    └ www/						 Web公開用ディレクトリ  
       └ run.py					 Web用中間アプリスクリプト  

なお、インスタンスの生成時及びe_STat_API_Adaptor.py内でこれらのディレクトリの設定を行えます。

## インスタンスの生成例
インスタンスの生成にはe-Stat APIのサイトで取得できるappIDが必要になります。
予め取得してください。

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import sys
    sys.path.append('./python')
    import e_Stat_API_Adaptor
    eStatAPI = e_Stat_API_Adaptor.e_Stat_API_Adaptor({
		# 取得したappId
		'appId'		: 'hogehoge'
		# データをダウンロード時に一度に取得するデータ件数
		,'limit'	: '10000'
		# next_keyに対応するか否か(非対応の場合は上記のlimitで設定した件数のみしかダウンロードされない)
		# 対応時はTrue/非対応時はFalse
		,'next_key'	: True
		# 中間アプリの設置ディレクトリ
		,'directory':'./'
		# APIのバージョン
		,'ver'		:'2.0'
    })

## 最初に行うこと
まず、ディレクトリ等を作成後に下記を実行してください。統計IDを検索するために必要なインデックスが生成されます。

    # 全ての統計表IDをローカルにダウンロード
    eStatAPI.load_all_ids()
    # ダウンロードした統計表IDからインデックスを作成 
    eStatAPI.build_statid_index()

また、下記を実行することで、STATISTICS_NAMEとTITLEから検索用インデックスを作成できます(N-gram形式)。
    
    eStatAPI.build_detailed_index()
    eStatAPI.search_detailed_index('家計')

## 機能

中間アプリの主な機能は下記の5つです。

### 統計IDの検索

インデックスリストを検索

    eStatAPI.search_id(
    	 '法人'
    	,eStatAPI.path['dictionary-index']
    )

    eStatAPI.search_id(
    	 'index'
    	,eStatAPI.path['dictionary-index']
    )
    
ユーザー作成型インデックスを検索

    eStatAPI.search_id(
    	 '法人'
    	,eStatAPI.path['dictionary-user']
    	,'user'
    )

    eStatAPI.search_id(
    	 '家計'
    	,eStatAPI.path['dictionary-index']
    )

下記でユーザー用のインデックスにすることも可能です。

    eStatAPI.create_user_index_from_detailed_index('法人')

### データのダウンロード
下記のようにget_csvメソッドを実行することで、
該当するデータがdata-cacheディレクトリ内にCSV形式で保存されます。

get_csvメソッドの返り値は保存されたCSVの1行目と3行目以降です。


    eStatAPI.get_csv(
    	 'get'
    	,'0000030002'
    )

作成されたCSVファイルは下記のようになります。  
1行目:列名  
2行目:キー  
3行目以降:データ(文字列)  

    "$","全国都道府県030001","男女Ａ030001","年齢各歳階級Ｂ030003","全域・集中の別030002","時間軸(年次)","unit"
    "$","area","cat02","cat03","cat01","time","unit"
    "117060396","全国","男女総数","総数","全域","1980年","人"

### データの表示
get_csvメソッドの第一引数に"get"を指定することでダウンロードした全てのデータを表示させることができます。

    eStatAPI.get_csv(
    	 'get'
    	,'0000030002'
    )

また、第一引数に"head"を指定するとデータの最初の5行、"tail"を指定すると最後の5行を表示させることができます。

    eStatAPI.get_csv(
    	 'head'
    	,'0000030001'
    )
    eStatAPI.get_csv(
    	 'tail'
    	,'0000030001'
    )

さらに、get_outputメソッドを使用することでJSON形式にデータを変換することができます。  
JSON形式にはCSVの行を基準としたjson-row形式(第二引数に"rjson"を指定)、列を基準としたjson-col形式(第二引数に"cjson"を指定)があります。
 
    eStatAPI.get_output(
    	　eStatAPI.get_csv('get' , '0000030001')
    	,'rjson'
    )

    [
    	 {全域・集中の別030002: "全域", 全国都道府県030001: "全国", 男女Ａ030001: "男女総数", 時間軸(年次): "1980年", 年齢５歳階級Ａ030002: "総数",…}
    	,{全域・集中の別030002: "全域", 全国都道府県030001: "全国市部", 男女Ａ030001: "男女総数", 時間軸(年次): "1980年", 年齢５歳階級Ａ030002: "総数",…}
	    …
	]
	
    eStatAPI.get_output(
    	　eStatAPI.get_csv('get' , '0000030001')
    	,'cjson'
    )
    
    {
    	$: [117060396, 89187409, 27872987, 5575989, 1523907, 1421927, 2082320, 1256745, 1251917,…]
    	unit: ["人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人",…]
    	全国都道府県030001: ["全国", "全国市部", "全国郡部", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県",…]
    	全域・集中の別030002: ["全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域",…]
    	年齢５歳階級Ａ030002: ["総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数",…]
    	時間軸(年次): ["1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年",…]
    }

### データの集約

2つの統計表を集約することもできます。
下記のように、第一引数に統計表ID(2つ)を「`,`」(カンマ)で区切って文字列として指定、第二引数にカテゴリ名(area等)、第三引数に集約する手法を指定してください。


    eStatAPI.merge_data(
    	 '0000030001,0000030001'
    	,'all'
    	,'std'
    )

なお、第三引数で指定できる集約する方法は下記になります。


|手法|   |
|---|---|
|最小値|min|
|最大値|max|
|中央値|median|
|頻度|count|
|分散|var|
|標準偏差|std|
|平均値|mean|
|合計|sum|



### データへのHTTPアクセス
UWSGIとFlaskを使用することでHTTPアクセスでデータを表示させ、取得することも可能です。
`www/run.py`を実行してください。

#### 取得

    リクエストURL 		: '<appId>/<cmd>/<id>.<ext>'
    <appID> 		: ご自身で取得されたApp IDです。
    <cmd>			: get、head、tailの3種類を指定できます。getの場合はデータ全体、headの場合はデータの上部一部分、tailはデータの下部一部分を表示します。
    <id>			: 取得したい統計データの統計表IDです。
    <ext>			: 取得したい出力形式です(「出力形式」を参照してください)。
    
    パラメーター
    dl			: 出力結果をダウンロードしたい場合はtrueを指定してください。

##### 例
「国勢調査(統計表ID:0000030001)」をCSV形式で表示する場合
   
    <appId>/get/0000030001.csv

「国勢調査(統計表ID:0000030001)」をCSV形式でダウンロードする場合
   
    <appId>/get/0000030001.csv?dl=true

#### 集約

    リクエストURL 	: '<appId>/merge/<ids>/<group_by>.<ext>'
    <appID> 	: ご自身で取得されたApp IDです。
    <ids>		: 結合したい2つの統計IDをカンマ区切りで指定します。
    <group_by>	: 集約したい列(キー)を指定します。area,time,cat01,cat02等になります。指定がない場合はallになります。
    <ext>		: 取得したい出力形式です(「出力形式」を参照してください)。
    
    パラメーター
    dl			: 出力結果をダウンロードしたい場合はtrueを指定してください。
    aggregate	: データを集約する手法を指定します。現在は下記の手法が対応しています。指定がない場合は全てのデータを表示します。


|手法|   |
|---|---|
|最小値|min|
|最大値|max|
|中央値|median|
|頻度|count|
|分散|var|
|標準偏差|std|
|平均値|mean|
|合計|sum|



##### 例
「国勢調査(統計表ID:0000030001,0000030002)」をマージしCSVで表示する場合

    /<appId>/merge/0000030001,0000030002/all.csv

「国勢調査(統計表ID:0000030001,0000030002)」をareaでマージしCSVで表示する場合

    /<appId>/merge/0000030001,0000030002/area.csv

「国勢調査(統計表ID:0000030001,0000030002)」をareaの平均値で集約しCSVで表示する場合

    /<appId>/merge/0000030001,0000030002/area.csv?aggregation=mean

#### 検索

    リクエストURL 	: '<appId>/search/<q>.<ext>'
    <appID> 	: ご自身で取得されたApp IDです。
    <q>			: 検索したい単語(一語)です。なお、「index」を指定すると全件表示されます。
    <ext>		: 取得したい出力形式です(「出力形式」を参照してください)。

    パラメーター
    dl			: 出力結果をダウンロードしたい場合はtrueを指定してください。

##### 例 
「法人」という単語が入った統計ID表をcsv形式で表示する場合

    /<appId>/search/法人.csv

「法人」という単語が入った統計ID表をcsv形式でダウンロードする場合

    /<appId>/search/法人.csv?dl=true

「法人」という単語が入った統計ID表を行型のJSON形式で表示する場合

    /<appId>/search/法人.rjson

「法人」という単語が入った統計ID表を列型のJSON形式で表示する場合

    /<appId>/search/法人.cjson

#### 出力形式
3つの出力形式があります。各リクエストURLにおいて「<ext>」で表されています。
なお、全てのエンコーディングはUTF-8になります。

1. csv  
csv形式の出力です。下記のようになります。
    
        "全域・集中の別030002","男女Ａ030001","年齢５歳階級Ａ030002","全国都道府県030001","時間軸(年次)","unit","$"
        "全域","男女総数","総数","全国","1980年","人","117060396"
        "全域","男女総数","総数","全国市部","1980年","人","89187409"
        "全域","男女総数","総数","全国郡部","1980年","人","27872987"
        "全域","男女総数","総数","北海道","1980年","人","5575989"
        "全域","男女総数","総数","青森県","1980年","人","1523907"
        "全域","男女総数","総数","岩手県","1980年","人","1421927"
        .....

2. rjson  
CSVを行単位でまとめたJSONの形式です。下記のようになります。

        [
    	 {全域・集中の別030002: "全域", 全国都道府県030001: "全国", 男女Ａ030001: "男女総数", 時間軸(年次): "1980年", 年齢５歳階級Ａ030002: "総数",…}
    	,{全域・集中の別030002: "全域", 全国都道府県030001: "全国市部", 男女Ａ030001: "男女総数", 時間軸(年次): "1980年", 年齢５歳階級Ａ030002: "総数",…}
	    …
	    ]

3. cjson  
CSVを列単位でまとめたJSONの形式です。下記のようになります。


        {
    	$: [117060396, 89187409, 27872987, 5575989, 1523907, 1421927, 2082320, 1256745, 1251917,…]
    	unit: ["人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人", "人",…]
    	全国都道府県030001: ["全国", "全国市部", "全国郡部", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県",…]
    	全域・集中の別030002: ["全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域", "全域",…]
    	年齢５歳階級Ａ030002: ["総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数", "総数",…]
    	時間軸(年次): ["1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年", "1980年",…]
        }


### 注意点
* データがキャッシュされているため、e-Stat API側でデータが変更された場合は、該当するデータのCSVファイルを削除して、再度ダウンロードしてください。