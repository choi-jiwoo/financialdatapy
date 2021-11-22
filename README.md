# financialdatapy

**financialdatapy** is a package for getting a fundamental financial data of a company. Currently it supports financial data of companies listed in United States (NASDAQ, NYSE). The user can see the company's latest financial statement reported, standard financials, and historical stock price. financialdatapy will be a good choice for research purposes, and making an investment portfolio.

## Installation

🪜🔨 on the process...

## Usage

🪵🪚 on the process...

### Financial statements

financialdatapy supports three major financial statements of a company. Income statement, balance sheet, and cash flow. Also the user can select between annual and quarter financial statements.

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

Financial statements reported by the company to a financial regulator. The elements in the financial statements are different from others, depending on the comapany.

```python
>>> from financialdatapy.stock import Stock
>>> comp = Stock('AAPL')
>>> ic_as_reported = comp.financials('income_statement', 'annual')
>>> ic_as_reported
```

```
|      CONSOLIDATED STATEMENTS OF OPERATIONS | 12 Months Ended                                 |
| USD ($) shares in Thousands, $ in Millions |   Sep. 26, 20xx | Sep. 28, 20xx | Sep. 29, 20xx |
|--------------------------------------------|-----------------|---------------|---------------|
|                                  Net sales |          xxxxxx |        xxxxxx |        xxxxxx |

```

#### STANDARD FINANCIAL STATEMENTS

Summarized financial statements of a company.

```python
>>> from financialdatapy.stock import Stock
>>> comp = Stock('AAPL')
>>> std_ic = comp.standard_financials('income_statement', 'annual')
>>> std_ic
```

```
|               |          TTM |    9/26/20xx| ... |
|---------------|--------------|-------------|-----|
| Total Revenue |       xxxxxx |       xxxxxx| ... |
```

## Stock data

### HISTORICAL STOCK DATA

Historical stock price of the company. ...

```python
>>> from financialdatapy.stock import Stock
>>> comp = Stock('AAPL')
>>> price = comp.historical('2021-1-1', '2021-1-5')
>>> price
```

```
|            |   close |    open |    high |     low |  volume |
|------------|---------|---------|---------|---------|---------|
| 20xx-01-04 | xxxx.xx | xxxx.xx | xxxx.xx | xxxx.xx | xxxxxxx |
| 20xx-01-05 | xxxx.xx | xxxx.xx | xxxx.xx | xxxx.xx | xxxxxxx |
```

</br >

All of the above will return in `pandas.DataFrame`.

## Documentation

🔩🔧 on the process...

## Credits

Data used in the package are from [SEC EDGAR](https://www.sec.gov/os/accessing-edgar-data), [finance.yahoo.com](https://finance.yahoo.com/), [investing.com](https://www.investing.com/).

## Disclaimer

financialdatapy is not meant to be used in trading. The data might not be accurate, and timely. So if you are willing to use data for trading, there are lot more better options.
