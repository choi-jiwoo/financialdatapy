import stocklist
import database
from decouple import config
import pandas as pd

if __name__ == '__main__':
    SQL_password = config('SQL_password', default='')
    db_name = 'us_stock'

    old_stock_list = stocklist.get_stock_list()
    db = database.Database(SQL_password, db_name)
    stock_list = db.read_db()
    stocklist.check_diff(old_stock_list, stock_list)

    # print(stock_list.head())