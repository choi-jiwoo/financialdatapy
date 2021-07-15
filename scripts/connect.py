import stocklist
import database
from decouple import config

mysql_pw = config('mysql_pw', default='')
db_name = 'us_stock'
table_name = 'stock_list'
# connect mysql server
db = database.Database(mysql_pw, db_name, table_name)
# get latest stock list data from source
latest_stock_list = stocklist.get_stock_list()

try:
    # save data in the database if doens't exists. If exists, raises a ValueError
    latest_stock_list.to_sql(table_name, db.engine, db_name, index=False)
    print("Success.")
except:
    print('Already in the database.')
finally:
    old_stock_list = db.read_table()
    diff = stocklist.check_diff(old_stock_list, latest_stock_list)

    # check if there is a difference
    if diff.empty:
        print("No difference")
    else :
        # update stock list to the latest
        db.delete_stock(diff)
        db.add_stock(diff)
    
