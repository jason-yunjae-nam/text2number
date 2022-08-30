import re
from typing import Dict, List


class NumberRegexExpression:
    INIT = "(?:^|\s)"
    UNIT = "([영일이삼사오육칠팔구]{1})"
    MTENS = "([십백천]{1})"
    MTENTHOUSANDS = "([만억조경해]{1})"


class RegularRegexExpression:
    TIME_REGEX = [
        # day, month, year
        "(?:^|\s)([영일이삼사오육칠팔구십백천만억]{1,})\s{0,}년",
        "(?:^|\s)([영일이삼사오육유칠팔구십시]{1,2})\s{0,}월[^하했할]", # "...사 월에는..."
        "(?:^|\s)[영일이삼사오육유칠팔구십시]{1,2}\s{0,}월\s{0,}([일이삼사오육칠팔구십]{1,})\s{0,}일[^일]", # "...구 월 이십일..."
        "(?:^|\s)([영일이삼사오육칠팔구십백천만억]{1,})\s{0,}년\s{0,}([일이삼사오육칠팔구십]{1,})\s{0,}일[^일]", # "...이천이십이년 이십일일..."
    ]

    MATH_REGEX = [
        '(?:^|\s)([영일이삼사오육칠팔구십백천만억조해경]{1,})\s{0,}점\s{0,}([영일이삼사오육칠팔구]{1,})\s{0,}(?:프로|점|퍼센트|그람|킬로|톤)', # "...구점 일 프로..."
        '(?:^|\s)([영일이삼사오육칠팔구십백천만억조해경]{1,})\s{0,}분의\s{0,}([영일이삼사오육칠팔구십백천만억조해경]{1,})',
    ]

    COUNT_REGEX = [
        # 제 _ 항/조 etc
        '(?:^|\s)제([영일이삼사오육칠팔구십백천만억조해경]{1,})\s{0,}(?:항|조|목|차관|조항|항목|관|회|차|법안심사)', # "...제 삼백칠십 항..."
        '(?:^|\s)전과\s{0,}([영일이삼사오육칠팔구십백천]{1,})\s{0,}범', # "...전과 구..."
        '(?:^|\s)([영일이삼사오육륙칠팔구십백천]{1,})\s{0,}다시\s{0,}([영일이삼사오육륙칠팔구십백천]{1,})',
    ]

    ID_NUMBER_REGEX = [
        '(?:^|\s)([공영일이삼사오육칠팔구]{2,3})\s{0,}([공영일이삼사오육칠팔구]{3,4})\s{0,}([공영일이삼사오육칠팔구]{4})', # "...공일공 이이이이 일일일일..."
        '(?:^|\s)([공영일이삼사오육칠팔구]{3})\s{0,}(?:다시|에)\s{0,}([공영일이삼사오육칠팔구]{2,4})\s{0,}(?:다시|에)\s{0,}([공영일이삼사오육칠팔구]{4,5})', # 사업자 번호
    ]

    REGULAR_REGEX = TIME_REGEX.copy()
    REGULAR_REGEX.extend(MATH_REGEX)
    REGULAR_REGEX.extend(COUNT_REGEX)
    REGULAR_REGEX.extend(ID_NUMBER_REGEX)


class MiscRegexExpression:
    MISC_REGEX: Dict[str, str] = {
        # 문자가 기호 등 으로 변환
        '[0-9](\s{0,}점\s{0,})[0-9]': ".", # "...6 점 5..."
        '[0-9](\s{0,}다시\s{0,})[0-9]': "-", # "...6 다시 5..."
        # '[0-9](\s*분의\s*)[0-9]' : "/",
    }


class RegexParser(NumberRegexExpression, RegularRegexExpression, MiscRegexExpression):
    def __init__(self):
        pass

def convert_regular_expression(sentence: str) -> str:
    for regex_num in CONVERT_REGEX:
        if regex_num in UNIT_REGEX:
            relaxed = True
        else:
            relaxed = False
        re_iter = re.finditer(regex_num, sentence)
        for s in re_iter:
            for i in reversed(range(1, len(s.groups())+1)):
                start = s.span(i)[0]
                end = s.span(i)[1]
                sentence = (
                    sentence[:start] 
                    + sentence[start:end].replace(s.group(i), txt_to_digit(s.group(i), relaxed)) 
                    + sentence[end:]
                )
    return sentence

def convert_text_regular_expression(sentence: str) -> str:
    for regex_text in CONVERT_TEXT_REGEX:
        re_iter_text = re.finditer(regex_text, sentence)
        for s in re_iter_text:
            for i in reversed(range(1, len(s.groups())+1)):
                start = s.span(i)[0]
                end = s.span(i)[1]
                sentence = (
                    sentence[:start] 
                    + sentence[start:end].replace(s.group(i), CONVERT_TEXT_REGEX[regex_text])
                    + sentence[end:]
                )
    return sentence

if __name__ == "__main__":
    items = [
        '내 전화번호는 공일공 이이이이 오오오오 입니다. 니 전화번호는 뭐니?',
        "광고 회사의 사업자등록번호를 조회하니 공공일다시공공다시사삼이이오가 조회 결과로 나왔다",
    ]
    for item in items:
        print(convert_regular_expression(item))
    None

