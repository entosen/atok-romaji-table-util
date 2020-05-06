import csv
import io
import jaconv
import pprint   # for debug
import re

reg_comment = re.compile(r'^\s*(#|$)')   # コメント・空行
reg_empty = re.compile(r'^\s*$')         # empty扱い

stroke_letters =  [ chr(code) for code in range(0x20, 0x7f+1)]

# stroke_dict[<stroke>] = <かな>   
# first_stroke_dict[<first_stroke>][<stroke>] = <かな>


def table2records(f):

    # コメント行、空行を除去
    valid_lines = []
    for line in f:
        if reg_comment.match(line):
            continue
        valid_lines.append(line)

    reader = csv.reader(valid_lines, 'excel-tab') 

    header_cols = []
    stroke_dict = {}
    for cols in reader:
        if cols[0] == 'HEADER':
            header_cols = cols[1:]
        else:
            stroke1 = cols[0] # TODO stroke を半角小文字化
            values = cols[1:]

            for i in range(len(values)):
                stroke2 = header_cols[i]
                v = values[i]
                if reg_empty.match(v):
                    continue
                stroke = stroke1 + (stroke2 if stroke2 != 'NULL' else '')
                if stroke in stroke_dict:
                    raise RuntimeErroro("すでにストロークが登録済み。{}".format(stroke))
                stroke_dict[stroke] = v

    return stroke_dict

def organize_by_first_stroke(stroke_dict):
    first_stroke_dict = {}

    for (stroke, kana) in stroke_dict.items():
        first_stroke = stroke[0]
        if first_stroke not in first_stroke_dict:
            first_stroke_dict[first_stroke] = {}
        first_stroke_dict[first_stroke][stroke] = kana

    return first_stroke_dict

# 特殊設定に対応するオプションを追加してもいいかも
def append_special_strokes(first_stroke_dict): 
    for (first_stroke, stroke_dict) in first_stroke_dict.items():

        # 子音連続で 'っ' にするストロークの追加
        # その first_stroke に含まれる stroke が、1strokeの1つのみの場合を除く
        # {'a': 'あ'} などは除く
        # {'ba': 'ば', 'bi': 'び', ... } などは追加
        if first_stroke not in stroke_dict:
            stroke_dict[first_stroke + '\u001f'] = 'っ'

            # さらに n の場合に限っては、n が余った場合に 'ん' にするストロークを追加
            if first_stroke == 'n':
                stroke_dict[first_stroke + '\u001e'] = 'ん'


def zen2han(input):
    # 半角カナにない特殊文字をまず変換
    buf = []
    for x in input:
        if x in ('ゐ', 'ヰ'):
            y = '\u0010'
        elif x in ('ゑ', 'ヱ'):
            y = '\u0011'
        elif x == 'ヵ':
            y = '\u0012'
        elif x == 'ヶ':
            y = '\u0013'
        elif x in ('ゎ', 'ヮ'):
            y = '\u0014'
        else:
            y = x
        buf.append(y)
    output = "".join(buf) 

    # 半角カタカナに変換
    output = jaconv.z2h(jaconv.hira2kata(output), kana=True, digit=True, ascii=True)
    output = output.replace('゛', 'ﾞ') # 全角濁点を半角濁点に 
    output = output.replace('゜', 'ﾟ') # 全角半濁点を半角半濁点に 
    return output


    
def prepare_to_pack(first_stroke_dict):
    # 総レコード数のカウント
    total_records = sum([len(records) for records in first_stroke_dict.values()])
    #print(total_records)
    if total_records > 550:
        raise RuntimeError(
                "total_records が550を超えています。total_records={}"
                .format(total_records))

    # stroke_letter 毎にレコード数とオフセットのカウント
    record_count_list = []
    offset = 0
    for c in stroke_letters:
        if c in first_stroke_dict:
            num = len(first_stroke_dict[c])
        else:
            num = 0
        record_count_list.append((offset, num))
        offset += num

    if offset != total_records:
        raise RuntimeError(
                "total_records({})と最終offset({})が一致しません。"
                .format(total_records, offset))

    # pprint.pprint(list(zip(stroke_letters, record_count_list)))
    record_list = []
    offset = 0
    for c in stroke_letters:
        if c not in first_stroke_dict:
            continue

        stroke_list = [t for t in first_stroke_dict[c].items()]
        stroke_list.sort()

        for (stroke, kana) in stroke_list:
            kana2 = zen2han(kana)
            record_list.append( (stroke, kana2, len(stroke), len(kana2), offset) )
            offset += len(stroke) + len(kana2)

    #pprint.pprint(record_list)
    return {
        'total_records': total_records,
        'record_count_list': record_count_list,
        'record_list': record_list
    }

def pack_to_style(first_stroke_dict):

    d = prepare_to_pack(first_stroke_dict)

    f = io.BytesIO()

    # 総バイト(4byte)
    f.write(d['total_records'].to_bytes(4, 'big'))

    # ヘッダ、固定値(4byte)
    f.write((0x01000002).to_bytes(4, 'big'))

    # stroke_letter 毎のレコード数とオフセット ((2byte+2byte) * 96letters = 384byte)
    for (offset, num) in d['record_count_list']:
        f.write(offset.to_bytes(2, 'big'))
        f.write(num.to_bytes(2, 'big'))

    # レコード長リスト ((2byte+1byte+1byte) * レコード数)
    for (stroke, kana, stroke_len, kana_len, offset) in d['record_list']:
        f.write(offset.to_bytes(2, 'big'))
        f.write(stroke_len.to_bytes(1, 'big'))
        f.write(kana_len.to_bytes(1, 'big'))

    # レコード内容
    for (stroke, kana, stroke_len, kana_len, offset) in d['record_list']:
        for c in stroke:
            f.write(ord(c).to_bytes(2, 'big'))
        for c in kana:
            f.write(ord(c).to_bytes(2, 'big'))

    return f.getvalue().hex()


