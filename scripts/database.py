from sqlalchemy import create_engine
import pymysql
import pandas as pd

class Database:
    def __init__(self, SQL_password, db_name) -> None:
        """connect to a database

        Args:
            SQL_password (string): relational database management system (RDBMS) password
            db_name (string): database to connect with 
        """
        self.engine = create_engine('mysql+mysqldb://root:'+SQL_password+'@localhost/'+db_name, encoding='utf-8')
        self.connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password=SQL_password,
                                    db=db_name)
        self.cursor = self.connection.cursor()

    def save_in_db(self, stock_list, table_name):
        """save received stock list in a database table

        Args:
            stock_list (dataframe): latest list of stock listed in US
            table_name (string): table name to save as
        """
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
        """close database connection
        """
        self.connection.close()