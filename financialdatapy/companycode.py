from financialdatapy.request import Request


def search_code(name: str) -> str:
    url = 'https://kind.krx.co.kr/common/searchcorpname.do'
    data = {
        'method': 'searchCorpNameJson',
        'searchCodeType': 'char',
        'searchCorpName': name,
    }
    headers = {
        'User-Agent': 'Mozilla',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = Request(url, method='post', headers=headers, data=data)
    comp_info_first_result = res.get_json()[0]
    company_code = comp_info_first_result['repisusrtcd2']

    return company_code
