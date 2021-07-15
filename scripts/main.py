import stocklist
import database
from decouple import config

if __name__ == '__main__':
    mysql_pw = config('mysql_pw', default='')
    db_name = 'us_stock'
    table_name = 'stock_list'
    # connect database server
    db = database.Database(mysql_pw, db_name)
    # create database if it's first time
    db.create_database()
    
    # get latest stock list data from source
    latest_stock_list = stocklist.get_stock_list()
    
    # check if table for stock list exists in the database
    ret = db.check_table_exists()
    if ret == 1:
        old_stock_list = db.read_db(table_name)
        diff = stocklist.check_diff(old_stock_list, latest_stock_list)

        # check if there is a difference
        if diff.empty:
            print("No difference")
        else :
            # update stock list to the latest
            db.delete_stock(table_name, diff)
            db.add_stock(table_name, diff)
    elif ret == 0:
        print('Stock list doensn\'t exists. Cannot compare the difference between past and latest stock list. \n Saving in progress.')
        db.save_in_db(latest_stock_list, table_name)

    