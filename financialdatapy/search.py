"""This module searches pair_id of a company from investing.com."""
from financialdatapy.request import Request


class Company:
    """A class representing a company name.

    :param symbol: Stock symbol to search its pair_id.
    :type symbol: str
    """

    def __init__(self, symbol: str) -> None:
        """Initialize Company."""
        self.symbol = symbol

    def search_pair_id(self) -> str:
        """Search pair_id of a company from investing.com.

        :return: pair_id of a company.
        :rtype: str
        """
        url = 'https://www.investing.com/search/service/searchTopBar'
        form_data = {
            'search_text': self.symbol,
        }
        res = Request(url, method='post', data=form_data)
        data = res.get_json()
        first_quote_result = data['quotes'][0]
        pair_id = first_quote_result['pairId']

        return pair_id
