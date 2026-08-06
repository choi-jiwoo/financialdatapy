from financialdatapy.stock import Stock


def main():
    stock = Stock("nvda")
    income_statement = stock.financials("income_statement", "annual")
    print(income_statement)


if __name__ == "__main__":
    main()
