# financialdatapy

`financialdatapy` is a package for getting a fundamental financial data of a company. Currently it supports financial
data of companies listed in United States (NASDAQ, NYSE) and South Korea (KOSPI, KOSDAQ).

User can see the company's latest financial statement reported, standard financials, and historical stock
price. `financialdatapy` will be a good choice for research purposes, and managing an investment portfolio.

## Installation

🪜🔨 on the process...

## Usage

🪵🪚 on the process...

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

##### United States Stock Exchange

##### Korea Stock Exchange

Financial statements reported by the company to a financial regulator. The elements in the financial statements are
different from others, depending on the comapany.

```python
>> > from financialdatapy.stock import Stock
>> > comp = Stock('AAPL')
>> > ic_as_reported = comp.financials('income_statement', 'annual')
>> > ic_as_reported
```

#### STANDARD FINANCIAL STATEMENTS

Summarized financial statements of a company.

```python
>> > from financialdatapy.stock import Stock
>> > comp = Stock('AAPL')
>> > std_ic = comp.standard_financials('income_statement', 'annual')
>> > std_ic
```

## Stock data

### HISTORICAL STOCK DATA

Historical stock price of the company. ...

```python
>> > from financialdatapy.stock import Stock
>> > comp = Stock('AAPL')
>> > price = comp.historical('2021-1-1', '2021-1-5')
>> > price
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
