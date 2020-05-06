import argparse
import pprint

import atok_romaji_table

def main():
    parser = argparse.ArgumentParser(
            description='子音×母音のマトリックスから、ATOKにインポート可能なローマ字テーブルを生成する')
    parser.add_argument('input', type=str,
                    help='input tab-separated matrix file.')
    args = parser.parse_args()

    with open(args.input, encoding='cp932') as f:
        stroke_dict = atok_romaji_table.table2records(f)
        
    #records = sorted(stroke_dict.items())  # stroke でソート
    #pprint.pprint(records)

    first_stroke_dict = atok_romaji_table.organize_by_first_stroke(stroke_dict)

    atok_romaji_table.append_special_strokes(first_stroke_dict)
    #pprint.pprint(first_stroke_dict)

    packed = atok_romaji_table.pack_to_style(first_stroke_dict)
    print(packed)

if __name__=='__main__':
    main()


