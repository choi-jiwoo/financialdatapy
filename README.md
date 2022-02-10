# financialdatapy

`financialdatapy` is a package for getting a fundamental financial data of a company. Currently it supports financial
data of companies listed in United States (NASDAQ, NYSE) and South Korea (KOSPI, KOSDAQ).

User can see the company's latest financial statement reported, standard financials, and historical stock
price. `financialdatapy` will be a good choice for research purposes, and managing an investment portfolio.

## Installation

🪜🔨 on the process...

## Quick Start

`financialdatapy` supports three major financial statements of a company. Income statement, balance sheet, and cash
flow. Also the user can select between annual and quarter financial statements.

### API Key

❗When getting financial statements of a company listed in Korea stock exchange, API Key
from [DART](https://opendart.fss.or.kr/) should be provided in the system to successfully retrieve its data.

After receiving API key, store it on a `.env` file in the root directory of your project.

Inside `.env` file.

```
DART_API_KEY=xxxxxxxxxxxxxxxx
```

### Initialization

```python
from financialdatapy.stock import Stock

# Apple
us_comp = Stock('aapl')
# Samsung Electronics
kor_comp = Stock('005930', country_code='kor')  # should set 'country_code' for stock exchange other than US
```

Values passed for financial statements and periods should follow the format below. If no argument is passed, it
automatically retrieves income statement from annual report.

```python
income_statement = us_comp.financials('income_statement')
balance_sheet = us_comp.financials('balance_sheet')
cash_flow = us_comp.financials('cash_flow')

# Annual Report
income_statement = kor_comp.financials('income-statement', 'annual')
# Quarterly Report
income_statement = kor_comp.financials('income-statement', 'quarter')
```

### Financial Statement as reported

Financial statements reported by the company to a financial regulator. The elements in the financial statements are
different from others, depending on the comapany and stock exchange.

**United States Stock Exchange**

```python
us_comp = Stock('aapl')
ic_as_reported = us_comp.financials('income_statement', 'annual')
```

**Korea Stock Exchange**

```python
kor_comp = Stock('005930', country_code='kor')
ic_as_reported = kor_comp.financials('income_statement', 'annual')
```

To see the full financial report from a browser, pass `True` in `web`. Supports both US exchange and KOR exchange.

```python
us_comp.financials(web=True)
kor_comp.financials(web=True)
```

### Standard Financial Statement

Summarized financial statements of a company.

```python
us_comp = Stock('msft')
std_ic = us_comp.standard_financials('income_statement', 'annual')
```

### Historical Stock Data

Historical stock price of the company.

```python
us_comp = Stock('aapl')
price = us_comp.price('2021-1-1', '2021-1-5')
```

All of the above will return in `pandas.DataFrame`.

## Contribute

It will be a great help if you contribute to the package. You can open
issues [here](https://github.com/cho2ji/financialdatapy/issues)

### Code style

The project basically follows [PEP-8](https://www.python.org/dev/peps/pep-0008/>)
, [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

### Git commit messages

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

The project basically follows Conventional Commits. Click on the badge to see the details.

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Documentation

The documentation is built with [Sphinx](https://www.sphinx-doc.org/en/master/index.html).

## License

Licensed under the MIT License

## Credits

Data used in the package are from [SEC EDGAR](https://www.sec.gov/os/accessing-edgar-data)
, [finance.yahoo.com](https://finance.yahoo.com/), [investing.com](https://www.investing.com/).

## Disclaimer

`financialdatapy` is not meant to be used in any kind of trading. The data might not be accurate, and timely.
`financialdatapy` is aimed for people who use stock data in their portfolio management and researchers who need stock
market data in their research. So if you are willing to use data for trading, there are lot more better options.
