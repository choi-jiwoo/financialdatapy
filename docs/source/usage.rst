Usage
=====

Main features of **financialdatapy** are getting the financial statement of
a company and its historical stock price data.

Example notebook can be found `here <https://github.com/choi-jiwoo/financialdatapy/tree/master/notebook>`_

Financial Statements as reported
--------------------------------

**Financial statements as reported of Apple (AAPL)**

.. code-block:: python

    from financialdatapy.stock import Stock

    aapl = Stock('aapl')

    default = aapl.financials()  # returns income statement of annual report

    # Annual report (10-K)
    ic_a = aapl.financials('income_statement', period='annual')
    bs_a = aapl.financials('balance_sheet', period='annual')
    cf_a = aapl.financials('cash_flow', period='annual')

    # Quarterly report (10-Q)
    ic_q = aapl.financials('income_statement', period='quarter')
    bs_q = aapl.financials('balance_sheet', period='quarter')
    cf_q = aapl.financials('cash_flow', period='quarter')

    # Open latest report in the web
    aapl.financials(web=True)  # annual report
    aapl.financials(period='quarter', web=True)  # quarterly report

**Financial statements as reported of Samsung Electronics (005930)**

.. note::
    API Key from `DART <https://opendart.fss.or.kr/>`_ is required to get the financial statements as reported of companies listed in Korea Exchange.

.. code-block:: python

    from financialdatapy.stock import Stock

    samsung = Stock('005930', country_code='kor')  # should specify 'country_code' for stock exchange other than USA

    default = samsung.financials()  # returns income statement of annual report

    # Annual report (사업보고서)
    ic_a = samsung.financials('income_statement', period='annual')
    bs_a = samsung.financials('balance_sheet', period='annual')
    cf_a = samsung.financials('cash_flow', period='annual')

    # Quarterly report (분기보고서)
    ic_q = samsung.financials('income_statement', period='quarter')
    bs_q = samsung.financials('balance_sheet', period='quarter')
    cf_q = samsung.financials('cash_flow', period='quarter')

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
    std_ic_a = msft.standard_financials('income_statement', period='annual')
    std_bs_a = msft.standard_financials('balance_sheet', period='annual')
    std_cf_a = msft.standard_financials('cash_flow', period='annual')

    # Quarterly
    std_ic_q = msft.standard_financials('income_statement', period='quarter')
    std_bs_q = msft.standard_financials('balance_sheet', period='quarter')
    std_cf_q = msft.standard_financials('cash_flow', period='quarter')

**Standard financial statement of Naver (035420)**

.. code-block:: python

    from financialdatapy.stock import Stock

    naver = Stock('035420', country_code='kor')  # should specify 'country_code' for stock exchange other than USA

    default = naver.standard_financials()  # returns income statement of annual report

    # Annual
    std_ic_a = naver.standard_financials('income_statement', period='annual')
    std_bs_a = naver.standard_financials('balance_sheet', period='annual')
    std_cf_a = naver.standard_financials('cash_flow', period='annual')

    # Quarterly
    std_ic_q = naver.standard_financials('income_statement', period='quarter')
    std_bs_q = naver.standard_financials('balance_sheet', period='quarter')
    std_cf_q = naver.standard_financials('cash_flow', period='quarter')

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

    sk_hynix = Stock('000660', country_code='kor')  # should specify 'country_code' for stock exchange other than USA

    default = sk_hynix.price()  # returns historical stock price of past 30 days from now.
    price = sk_hynix.price('2021-1-1', '2021-1-5')  # pass date string format as YYYY-MM-DD

List of Companies in Stock Exchange
-----------------------------------

**United States Stock Exchange**

.. code-block:: python

    from financialdatapy.stocklist import UsStockList

    us_stock_list = UsStockList().get_stock_list()


**Korea Stock Exchange**

Api key is required to get the stock list of companies in Korea stock exchange. See more about the api key in the **API
Key** section above.

.. code-block:: python

    from financialdatapy.stocklist import KorStockList

    kor_stock_list = KorStockList().get_stock_list()

Getting CIK of US Companies
---------------------------

CIK is defined by `SEC <https://www.sec.gov/edgar/searchedgar/cik.htm>`_ as

    The **Central Index Key (CIK)** is used on the SEC's computer systems to identify corporations and individual people who have filed disclosure with the SEC.

.. code-block:: python

    from financialdatapy.stocklist import UsStockList

    apple_ticker = 'AAPL'
    us_stock_list = UsStockList()
    apple_cik = us_stock_list.search_cik(apple_ticker)

Getting Stock Code of KOR Companies
-----------------------------------

A **stock code** is equivalent to the term `ticker`, used in Korea Exchange.

.. code-block:: python

    from financialdatapy.stocklist import KorStockList

    samsung_elec = '삼성전자'
    samsung_elec_stock_code = KorStockList.search_stock_code(samsung_elec)
