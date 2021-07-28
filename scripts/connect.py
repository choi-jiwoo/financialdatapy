import database
from decouple import config

def connect_db():
    mysql_pw = config('mysql_pw', default='')
    db_name = 'us_stock'
    table_name = 'stock_list'
    try:
        db = database.Database(mysql_pw, db_name, table_name)
        return db
    except Exception as e:
        print(e)
