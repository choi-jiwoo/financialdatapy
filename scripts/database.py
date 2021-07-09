from sqlalchemy import create_engine
import pymysql
import pandas as pd

class Database:
    def __init__(self, SQL_password, db_name) -> None:
        self.engine = create_engine('mysql+mysqldb://root:'+SQL_password+'@localhost/'+db_name, encoding='utf-8')
        self.connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password=SQL_password,
                                    db=db_name)
        self.cursor = self.connection.cursor()

    def save_in_db(self, stock_list, table_name):
        try:
            stock_list.to_sql(table_name, self.engine, index=False)
            print("Success!")
        except Exception as e:
            print(e)

    def read_db(self):
        try:
            stock_list = pd.read_sql_table('us_stock', self.engine)
            return stock_list
        except Exception as e:
            print(e)
    
    def __del__(self):
        self.connection.close()