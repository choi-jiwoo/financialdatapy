from decouple import config
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import stocklist

def save_in_db():
    stock_list = stocklist.get_stock_list()
    db_name = 'us_stock'
    SQL_password = config('SQL_password', default='')
    engine = create_engine('mysql+mysqldb://root:'+SQL_password+'@localhost/'+db_name, encoding='utf-8')
    connection = pymysql.connect(host='localhost',
                         user='root',
                         password=SQL_password,
                         db=db_name)
    cursor = connection.cursor()
    try:
        stock_list.to_sql(db_name, engine, index=False)
        print("Success!")
    except Exception as e:
        print(e)
    finally:
        # connection.commit()
        connection.close()