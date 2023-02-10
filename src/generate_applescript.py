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

    # print(stroke_dict)

    print(textwrap.dedent('''\
        tell application "ATOK Customizer"
            activate
        end tell
        '''))

    print('tell application "System Events"')

    for k,v in stroke_dict.items():
        print(textwrap.dedent('''\
            key code 49 -- Space
            set the clipboard to "%s"
            keystroke "v" using {command down}
            delay 0.5
            
            key code 48 -- Tab
            set the clipboard to "%s"
            keystroke "v" using {command down}
            delay 0.5
            
            key code 36 -- Enter
            delay 0.5

            ''') % (k,v))

    print('end tell')

if __name__=='__main__':
    main()



