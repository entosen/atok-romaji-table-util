########################################################
atok-romaji-table-util
########################################################

Utility scripts to import/export ATOK romaji table.

ATOKローマ字テーブルをインポート/エクスポートするための便利スクリプト。


ATOKでAZIK風のローマ字テーブルにしたかったが、
ATOKのローマ字テーブルの編集が使いづらかったのでスクリプトを書いた。


- decode_atok_romaji.py

  - ATOKのスタイルファイル中のローマ字テーブルを人が読める形にデコードする

- encode_romaji_matrix.py

  - 子音×母音のマトリックスから、ATOKにインポート可能なローマ字テーブルを生成する


ATOK for Mac にローマ字テーブルを流し込むスクリプトを作りました。

- :doc:`doc/romaji_feed_mac.rst`


準備
=========

::

    py -m pip install jaconv


使い方
=========


decode_atok_romaji.py
---------------------------

ATOKのスタイルファイル中のローマ字テーブルを人が読める形にデコードする。

手順

#. ATOKプロパティ ＞ 「キー・ローマ字・色」タブ
#. デコードしたいスタイルを選択し、スタイル操作 ＞ ファイルに出力 ＞ 適当なフォルダ・ファイル名で保存
#. 以下のように実行::

       py src/decode_atok_romaji.py <保存した.STYファイル>

#. 標準出力にデコード結果が出力される

出力例(AZIKの例) → `sample/output_decode_atok_romaji.txt <sample/output_decode_atok_romaji.txt>`__





encode_romaji_matrix.py
----------------------------

子音×母音のマトリックスから、ATOKにインポート可能なローマ字テーブルを生成する。

手順

#. 子音×母音のマトリックスファイルを用意する

   .. image:: doc/fig/romaji_matrix_AZIK_fig.png
       :height: 300px

   - サンプルファイル→ `sample/romaji_matrix_AZIK.txt <sample/romaji_matrix_AZIK.txt>`__
   - 区切りはタブ
   - 詳細なフォーマットは、`doc/format_romaji_matrix.rst <doc/format_romaji_matrix.rst>`__ を参照

#. 以下のように実行::

       py src/encode_romaji_matrix.py <子音×母音のマトリックスファイル>

#. 標準出力に出力される

   - 出力例(AZIKの場合の例) → `sample/atok_romaji_AZIK.txt <sample/atok_romaji_AZIK.txt>`__

#. ATOKのスタイルを一旦ファイルに出力し、それの「ローマ字=」の部分をテキストエディタで上記出力結果に置き換える

    (#) ATOKプロパティ ＞ 「キー・ローマ字・色」タブ
    (#) デコードしたいスタイルを選択し、スタイル操作 ＞ ファイルに出力 ＞ 適当なフォルダ・ファイル名で保存

#. 変更後のスタイルファイルをATOKに読み込ませる
  
    (#) ATOKプロパティ ＞ 「キー・ローマ字・色」タブ
    (#) スタイル操作 ＞ ファイルを指定して追加




謝辞
=====

参考にさせていただいたサイト

- ATOKのファイルフォーマット

  - `ATOK2008 .styファイル覚え書き hossy online - といぼっくす <https://hossy.info/?date=1105>`__

- 利用させていただいたライブラリ

  - `jaconv · PyPI <https://pypi.org/project/jaconv/0.2/>`__




開発にあたって
=================

PR,Issue大歓迎。

- 主にWindowsで使うことを想定しているので

  - 改行コードは原則 crlf で。(問題が出たら考える)

    - 一部 lf のファイルがあるかも
    - 基本的に既存ファイルの改行コードを踏襲してください
    - ``git config core.autocrlf false`` 推奨

  - 文字コード

    - python のソースコードは utf-8
    - 入出力のファイルは cp932 が混在している

