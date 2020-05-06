import argparse
import io
import re

re_romaji = re.compile("^ローマ字=")
key_names = []
for ci in range(0x20, 0x7f+1):
    if ci == 0x20: # Space
        name = "SP"
    elif ci == 0x7f: # DEL
        name = "DEL"
    else:
        name = chr(ci)
    key_names.append(name)


def load_romaji_data(input, encoding='shift-jis'):
    with open(input, 'r', encoding=encoding) as f:
        for line in f:
            if re_romaji.match(line):
                tmp = line.rstrip()
                tmp = re_romaji.sub('', tmp, 1)
                return tmp

    raise RuntimeError("'ローマ字='の行が見つかりませんでした。")

def decode_romaji(romaji_bytes):
    f = io.BytesIO(romaji_bytes)

    # レコード数
    roman_num_b = f.read(4)
    roman_num = int.from_bytes(roman_num_b, 'big')
    print("roman_num=%d (%s)" % (roman_num, roman_num_b.hex()))

    version_b = f.read(4)
    print("version?=%s" % version_b.hex())

    print("先頭キー別レコードオフセット、レコード数")
    for key_name in key_names:
        offset = int.from_bytes(f.read(2), 'big')
        num = int.from_bytes(f.read(2), 'big')
        print("%s\t%d\t%d" % (key_name, offset, num))

    print("レコード毎キー情報オフセット、キー長")
    keylen_info_list = []
    for i in range(roman_num):
        offset = int.from_bytes(f.read(2), 'big')
        in_len = int.from_bytes(f.read(1), 'big')
        out_len = int.from_bytes(f.read(1), 'big')
        keylen_info_list.append( (offset, in_len, out_len) )
        print("%d\t%d\t%d\t%d" % (i, offset, in_len, out_len))

    print("レコード情報")
    i_record=0
    for (offset, in_len, out_len) in keylen_info_list:
        in_chars = []
        in_hexs = []
        out_chars = []
        out_hexs = []
        for j in range(in_len):
            in_bytes = f.read(2)
            in_hexs.append(in_bytes.hex())
            code = int.from_bytes(in_bytes, 'big')
            c = chr(code)
            in_chars.append(c)
        for k in range(out_len):
            out_bytes = f.read(2)
            out_hexs.append(out_bytes.hex())
            code = int.from_bytes(out_bytes, 'big')
            c = chr(code)
            out_chars.append(c)
        print("%d\t%d\t%s\t(%s)\t%s\t(%s)" 
                % (i_record, offset, 
                    "".join(in_chars), " ".join(in_hexs),
                    "".join(out_chars), " ".join(out_hexs)))
        i_record += 1


    end = f.read()
    if len(end) > 0 :
        raise RuntimeException("format error")


def main():
    parser = argparse.ArgumentParser(
            description='ATOKのスタイルファイル中のローマ字テーブルを人が読める形にデコードする')
    parser.add_argument('input', type=str,
                    help='input file. ATOKスタイルファイル(.STY)')
    args = parser.parse_args()

    romaji_hexs = load_romaji_data(args.input)
    romaji_bytes = bytes.fromhex(romaji_hexs)
    decode_romaji(romaji_bytes)

if __name__ == "__main__":
    main()
