# financialdatapy

`financialdatapy` is a package for getting a fundamental financial data of a company. Currently it supports financial
data of companies listed in United States (NASDAQ, NYSE) and South Korea (KOSPI, KOSDAQ).

User can see the company's latest financial statement reported, standard financials, and historical stock
price. `financialdatapy` will be a good choice for research purposes, and managing an investment portfolio.

## Installation

🪜🔨 on the process...

## Usage

🪵🪚 on the process...

### Initialization

```python
from financialdatapy.stock import Stock

us_comp = Stock('aapl')
kor_comp = Stock('005930', country_code='kor')  # should set 'country_code' for stock exchange other than US
```

### Financial statements

financialdatapy supports three major financial statements of a company. Income statement, balance sheet, and cash flow.
Also the user can select between annual and quarter financial statements.

Values passed for financial statements and periods should follow the format below.

Financial statements:

| Financial statement | Value              |
| ------------------- | ------------------ |
| Income statement    | `income_statement` |
| Balance sheet       | `balance_sheet`    |
| Cash flow           | `cash_flow`        |

Periods:

| Period  | Value     |
| ------- | --------- |
| Annual  | `annual`  |
| Quarter | `quarter` |

#### FINANCIAL STATEMENTS AS REPORTED

Financial statements reported by the company to a financial regulator. The elements in the financial statements are
different from others, depending on the comapany.

##### United States Stock Exchange

```python
from financialdatapy.stock import Stock

us_comp = Stock('aapl')
ic_as_reported = us_comp.financials('income_statement', 'annual')
```

##### Korea Stock Exchange

#### STANDARD FINANCIAL STATEMENTS

Summarized financial statements of a company.

```python
from financialdatapy.stock import Stock

us_comp = Stock('aapl')
std_ic = us_comp.standard_financials('income_statement', 'annual')
```

## Stock data

### HISTORICAL STOCK DATA

Historical stock price of the company. ...

```python
from financialdatapy.stock import Stock

us_comp = Stock('aapl')
price = us_comp.price('2021-1-1', '2021-1-5')
```

All of the above will return in `pandas.DataFrame`.

## Documentation

🔩🔧 on the process...

## Credits

Data used in the package are from [SEC EDGAR](https://www.sec.gov/os/accessing-edgar-data)
, [finance.yahoo.com](https://finance.yahoo.com/), [investing.com](https://www.investing.com/).

## Disclaimer

`financialdatapy` is not meant to be used in any kind of trading. The data might not be accurate, and timely.
`financialdatapy` is aimed for people who use stock data in their portfolio management and researchers who need stock
market data in their research. So if you are willing to use data for trading, there are lot more better options.
