import stocklist
import database
from decouple import config

if __name__ == '__main__':
    SQL_password = config('SQL_password', default='')
    db_name = 'us_stock' # same db and table name
    db = database.Database(SQL_password, db_name)
    
    # get stock list data from source
    latest_stock_list = stocklist.get_stock_list()
    
    # check if stock list is in the database
    ret = db.check_table_exists()
    if ret == 1:
        old_stock_list = db.read_db()
        diff = stocklist.check_diff(old_stock_list, latest_stock_list)

        if diff.empty:
            print("No difference")
        else :
            # update stock list to the latest
            db.delete_stock(db_name, diff)
            db.add_stock(db_name, diff)
    elif ret == 0:
        print('Stock list doensn\'t exists. Cannot compare the difference between past and latest stock list. \n Saving in progress.')
        db.save_in_db(latest_stock_list, db_name)

    