import argparse
import pprint
import textwrap

import atok_romaji_table

def main():
    parser = argparse.ArgumentParser(
            description='子音×母音のマトリックスから、ATOKにインポート可能なローマ字テーブルを生成する')
    parser.add_argument('input', type=str,
                    help='input tab-separated matrix file.')
    args = parser.parse_args()

    with open(args.input, encoding='cp932') as f:
        stroke_dict = atok_romaji_table.table2records(f)


    print(textwrap.dedent('''\
        -- あらかじめ、下記の設定を ON にしておく
        -- - システム環境設定 > キーボード > ショートカット > コントロール間のフォーカス移動をキーボードで操作 > ON
        --
        -- スクリプトエディタを起動し、このスクリプトを開く (まだ実行しない)
        -- 
        -- ATOK キー・ローマ字カスタマイザを起動
        -- ローマ字テーブルが空のスタイルを1つ用意する
        -- 「ローマ字設定ボタン」
        -- Tabキーを何度か押して、「＋」ボタンにフォーカスがある状態にする
        --
        -- IME を OFF (英字入力) にしておく
        -- 
        -- スクリプトエディタで、このスクリプトを実行
        '''))

    print(textwrap.dedent('''\
        tell application "ATOK Customizer"
            activate
        end tell
        '''))

    print(textwrap.dedent('''\
        on addRomaji(roman, kana)
            tell application "System Events"
                
                key code 49 -- Space で "+" ボタン押下
                delay 0.25
                
                -- ローマ字の入力欄にフォーカスがある
                keystroke roman
                
                key code 48 -- Tab で かな の入力欄にフォーカスを移動
                set the clipboard to kana
                keystroke "v" using {command down}
                delay 0.25
                
                key code 36 -- Enter
                delay 0.25
                
            end tell
        end addRomaji
        '''))

    for k,v in stroke_dict.items():
        print(f'addRomaji("{k}", "{v}")')

if __name__=='__main__':
    main()



