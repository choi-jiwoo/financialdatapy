from scripts import cik
from scripts import filings


CIK_LIST = cik.get_cik()


class Stock():
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def get_financials(self):
        pass

    def std_financials(self):
        pass
