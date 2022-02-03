from financialdatapy import request


class Company:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def search_pair_id(self) -> str:
        url = 'https://www.investing.com/search/service/searchTopBar'
        form_data = {
            'search_text': self.symbol,
        }
        res = request.Request(url, method='post', data=form_data)
        data = res.get_json()
        pair_id = data['quotes'][0]['pairId']

        return pair_id
