#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import e_Stat_API_Adaptor
import sys
sys.path.append('./')

eStatAPI = e_Stat_API_Adaptor.PythonAdaptor({
    'appId': '#appID#',  # 取得したappId
    'limit': '10000',  # データをダウンロード時に一度に取得するデータ件数
    'next_key': True,  # next_keyに対応するか否か(非対応の場合は上記のlimitで設定した件数のみしかダウンロードされない)# 対応時はTrue/非対応時はFalse
    'directory': '#Directory#',  # 中間アプリの設置ディレクトリ
    'ver': '2.0'       # APIのバージョン
})
# 0000030001をcsvの形式でダウンロード
print('id:' + sys.argv[1])
print(eStatAPI.get_csv('get', sys.argv[1]))
