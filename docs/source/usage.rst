Usage
=====

The main features of **financialdatapy** is getting the financial statement of
a company and its historical stock price data.

Financial Statement as reported
-------------------------------

**Financial statement as reported of Apple (AAPL)**

.. code-block:: python

    from financialdatapy.stock import Stock

    aapl = Stock('aapl')

    default = aapl.financials()  # returns income statement of annual report

    # Annual report (10-K)
    ic_a = aapl.financials('income_statement', 'annual')
    bs_a = aapl.financials('balance_sheet', 'annual')
    cf_a = aapl.financials('cash_flow', 'annual')

    # Quarterly report (10-Q)
    ic_q = aapl.financials('income_statement', 'quarter')
    bs_q = aapl.financials('balance_sheet', 'quarter')
    cf_q = aapl.financials('cash_flow', 'quarter')

    # Open latest report in the web
    aapl.financials(web=True)  # annual report
    aapl.financials(period='quarter', web=True)  # quarterly report

**Financial statement as reported of Samsung Electronics (005930)**

.. code-block:: python

    from financialdatapy.stock import Stock

    samsung = Stock('005930', 'kor')  # should specify 'country_code' for stock exchange other than USA

    default = samsung.financials()  # returns income statement of annual report

    # Annual report (사업보고서)
    ic_a = samsung.financials('income_statement', 'annual')
    bs_a = samsung.financials('balance_sheet', 'annual')
    cf_a = samsung.financials('cash_flow', 'annual')

    # Quarterly report (분기보고서)
    ic_q = samsung.financials('income_statement', 'quarter')
    bs_q = samsung.financials('balance_sheet', 'quarter')
    cf_q = samsung.financials('cash_flow', 'quarter')

    # Open latest report in the web
    samsung.financials(web=True)  # annual report
    samsung.financials(period='quarter', web=True)  # quarterly report

Standard Financial Statement
----------------------------

**Standard financial statement of Microsoft (MSFT)**

.. code-block:: python

    from financialdatapy.stock import Stock

    msft = Stock('msft')

    default = msft.standard_financials()  # returns income statement of annual report

    # Annual
    std_ic_a = msft.standard_financials('income_statement', 'annual')
    std_bs_a = msft.standard_financials('balance_sheet', 'annual')
    std_cf_a = msft.standard_financials('cash_flow', 'annual')

    # Quarterly
    std_ic_q = msft.standard_financials('income_statement', 'quarter')
    std_bs_q = msft.standard_financials('balance_sheet', 'quarter')
    std_cf_q = msft.standard_financials('cash_flow', 'quarter')

**Standard financial statement of Naver (035420)**

.. code-block:: python

    from financialdatapy.stock import Stock

    naver = Stock('035420', 'kor')  # should specify 'country_code' for stock exchange other than USA

    default = naver.standard_financials()  # returns income statement of annual report

    # Annual
    std_ic_a = naver.standard_financials('income_statement', 'annual')
    std_bs_a = naver.standard_financials('balance_sheet', 'annual')
    std_cf_a = naver.standard_financials('cash_flow', 'annual')

    # Quarterly
    std_ic_q = naver.standard_financials('income_statement', 'quarter')
    std_bs_q = naver.standard_financials('balance_sheet', 'quarter')
    std_cf_q = naver.standard_financials('cash_flow', 'quarter')

Historical Stock Data
---------------------

**Historical stock price of Snowflake (SNOW)**

.. code-block:: python

    from financialdatapy.stock import Stock

    snowflake = Stock('snow')

    default = snowflake.price()  # returns historical stock price of past 30 days from now.
    price = snowflake.price('2021-1-1', '2021-1-5')  # pass date string format as YYYY-MM-DD

**Historical stock price of SK Hynix (000660)**

.. code-block:: python

    from financialdatapy.stock import Stock

    sk_hynix = Stock('000660', 'kor')  # should specify 'country_code' for stock exchange other than USA

    default = sk_hynix.price()  # returns historical stock price of past 30 days from now.
    price = sk_hynix.price('2021-1-1', '2021-1-5')  # pass date string format as YYYY-MM-DD

List of Companies in Stock Exchange
-----------------------------------

**United States Stock Exchange**

.. code-block:: python

    from financialdatapy.stocklist import UsStockList

    stock_list = UsStockList().get_stock_list()


**Korea Stock Exchange**

Api key is required to get the stock list of companies in Korea stock exchange. See more about the api key in the **API
Key** section above.

.. code-block:: python

    from financialdatapy.stocklist import KorStockList

    stock_list = KorStockList().get_stock_list()
