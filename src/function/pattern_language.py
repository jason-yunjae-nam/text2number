import re
from typing import Dict
from function import *

TIME_REGEX = [
    # day, month, year
]

UNIT_REGEX = [
    # percent, gram, kilo, etc
]

COUNT_REGEX = [
    # 제 _ 항/조 etc
]

REVERT_REGEX = [
    # 아라비아 숫자를 한글로 변환
]

REGEX_NUMBERS_AFTER_CONVERT = [
    '([가-힣|0-9]+)\s*점\s*[가-힣|0-9]+\s*(프로|점|퍼센트|그람|킬로)',
    '[가-힣|0-9]+\s*점\s*([가-힣|0-9]+)\s*(프로|점|퍼센트|그람|킬로)',
    '\s제([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조|해|경]{1,})\s*[항|조|목|차관|조항|항목|관|회|차|법안심사]',
    '^제([영|일|이|삼|사|오|육|칠|팔|구|십|백|천|만|억|조|해|경]{1,})\s*[항|조|목|차관|조항|항목|관|회|차|법안심사]',
    
    # '\s제([가-힣]+)\s*[항|조|목|차관|조항|항목|관|회|차|법안심사]',
    '전과\s{0,1}([영|일|이|삼|사|오|육|칠|팔|구|십|백|천]{1,})\s{0,1}범',
]

PASS_NUMBERS = [
    '([0|1|2|3|4|5|6|7|8|9|10]{1})\s*시', #[몇]시
]

REGEX_NUMBERS_BEFORE_CONVERT = [
    '[가-힣|0-9]+\s{0,1}월\s{0,1}([가-힣|0-9]+[일]*)\s{0,1}(일+)',
    '[가-힣|0-9]+\s{0,1}년\s{0,1}([가-힣|0-9]+[일]*)\s{0,1}(일+)'
]

REGEX_TEXT_CORRECTIONS: Dict[str, str] = {
    '[0-9\s](\s*[점]\s+)[0-9]': ".",
}

def apply_regular_expression_before_convert(sentence):
    for regex_num in REGEX_NUMBERS_BEFORE_CONVERT:
        # regexp = re.compile(regex_num)
        re_iter = re.finditer(regex_num, sentence)
        for s in re_iter:
            sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), get_number(s.group(1))) + sentence[s.end():]
    return sentence

def apply_regular_expression(sentence: str) -> str:
    for regex_num in REGEX_NUMBERS_AFTER_CONVERT:
        re_iter = re.finditer(regex_num, sentence)
        for s in re_iter:
            sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), get_number(s.group(1))) + sentence[s.end():]
    for regex_text in REGEX_TEXT_CORRECTIONS:
        re_iter_text = re.finditer(regex_text, sentence)
        for s in re_iter_text:
            sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), REGEX_TEXT_CORRECTIONS[regex_text]) + sentence[s.end():]
    return sentence

# def pass_numbers(sentence: str) -> str:
#     for regex in PASS_NUMBERS:
#         re_iter = re.finditer(regex, sentence)
#         for s in re_iter:
#             sentence = sentence[:s.start()] + sentence[s.start():s.end()].replace(s.group(1), get_txt(s.group(1))) + sentence[s.end():]
#     return sentence


if __name__ == "__main__":
    # print(apply_regular_expression('제육 조 제이십사 항을 참고바랍니다.'))
    # print(apply_regular_expression("나는 이번 유 월 사일에 본 시험에서 9점 4점을 받았어."))
    # print(apply_regular_expression("네 유월 이십이 일이면 상당히 늦은 시점이었지만 그래도 완료가 되었다."))
    items = [
        "나는 전과 구범 이야.",
        "여기서 누구가 전과 백범 이야?",
        "여기서 누구가 전과 이십오범 이야?",
    ]
    for i in items:
        print(apply_regular_expression(i))
    None
