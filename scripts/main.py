import stocklist
import database
from decouple import config
import pandas as pd

if __name__ == '__main__':
    SQL_password = config('SQL_password', default='')
    db_name = 'us_stock'
    # stocklist.get_stock_list()
    db = database.Database(SQL_password, db_name)
    stock = db.read_db()
    print(stock.head())