import argparse
import pprint
import sys
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

    
    sys.stdout.buffer.write(b'\xEF\xBB\xBF')  # bom付きutf-8にするため

    print(textwrap.dedent('''\
        # このファイルは BOM 付きの UTF-8 で保存されないといけません
        # 
        # PCの負荷が高いと流し込みを取りこぼすことがあります。できるだけ下記を行ってください。
        # - 設定 > 簡単操作 > ディスプレイ > Windows にアニメーションを表示する > OFF
        # - できるだけ他のアプリケーションを終了させる
        # - スクリーン・セーバーや画面ロックをOFFにしておく
        # 
        # ATOKプロパティ > キー・ローマ字・色
        # - ローマ字カスタマイズが空のスタイルを1つ用意する
        # - 「ローマ字カスタマイズ」ボタン
        #
        # powershell で、このスクリプトを実行
        # 5秒以内に、ローマ字カスタマイズのダイアログをクリックし全面に出す
        '''))

    print(textwrap.dedent('''\
        Add-Type -AssemblyName Microsoft.VisualBasic
        Add-Type -AssemblyName System.Windows.Forms
        '''))

    print(textwrap.dedent('''\
        function AddRomaji($roman, $kana) {
            [System.Windows.Forms.SendKeys]::SendWait("%A")
            sleep -Milliseconds 10

            Set-Clipboard -Value "$roman"
            sleep -Milliseconds 10
            [System.Windows.Forms.SendKeys]::SendWait("%R")
            sleep -Milliseconds 10
            [System.Windows.Forms.SendKeys]::SendWait("^V")
            sleep -Milliseconds 10

            Set-Clipboard -Value "$kana"
            sleep -Milliseconds 10
            [System.Windows.Forms.SendKeys]::SendWait("%K")
            sleep -Milliseconds 10
            [System.Windows.Forms.SendKeys]::SendWait("^V")
            sleep -Milliseconds 10

            [System.Windows.Forms.SendKeys]::SendWait("{Enter}")
            sleep -Milliseconds 10
        }
        '''))

    print(f'sleep -Seconds 5')
    print()

    for k,v in stroke_dict.items():
        print(f'AddRomaji "{k}"  "{v}"')

if __name__=='__main__':
    main()




