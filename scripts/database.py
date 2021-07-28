from sqlalchemy import create_engine
import pymysql
import pandas as pd

class Database:
    def __init__(self, mysql_pw, db_name, table_name) -> None:
        """connect to a mysql server

        Args:
            mysql_pw (string): relational database management system (RDBMS) password
            db_name (string): database name to work in
            table_name (string): table name to work in
        """
        self.db_name = db_name
        self.table_name = table_name
        self.engine = create_engine('mysql+mysqldb://root:'+mysql_pw+'@localhost/', encoding='utf-8')
        self.connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password=mysql_pw)
        self.cursor = self.connection.cursor()

        query = f'CREATE DATABASE IF NOT EXISTS {self.db_name}'
        self.cursor.execute(query)
        self.connection.commit

        query = f'USE {self.db_name}'
        self.cursor.execute(query)

        
    def save_in_db(self, latest_stock_list):
        """save latest stock list in database

        Args:
            latest_stock_list (dataframe): latest stock list
        """
        try:
            # If database exists, raises a ValueError
            latest_stock_list.to_sql(
                self.table_name, 
                self.engine, 
                self.db_name, 
                ndex=False
            )
            print("Success.")
        except:
            print('Already in the database.')
        finally:
            old_stock_list = self.read_table()
            merged = pd.merge(old_stock_list, 
                latest_stock_list, 
                how='outer', 
                indicator=True
            )
            diff = merged[merged['_merge'] != 'both']

            if diff.empty:
                print("No difference") # 21/7/28 : do i need this?
            else :
                self.delete_stock(diff)
                self.add_stock(diff)

    def read_table(self):
        """get stock list saved in the database

        Returns:
            dataframe: stock list saved in the database
        """
        try:
            stock_list = pd.read_sql_table(self.table_name, self.engine, self.db_name)
            return stock_list
        except Exception as e:
            print(e)

    def delete_stock(self, diff):
        """delete stocks from stock list database which are unlisted from stock exchange

        Args:
            diff (dataframe): dataframe that stores which stocks are unlisted and newly listed
        """
        # stocks only in past stock list
        old = diff[diff['_merge']=='left_only']
        
        try:
            for i in old['Symbol']:
                query = f'DELETE FROM {self.table_name} WHERE Symbol=%s'
                self.cursor.execute(query, i)

            self.connection.commit()

        except Exception as e:
            print(e)

    def add_stock(self, diff):
        """add stocks to stock list database wihch are newly listed in stock exchange

        Args:
            diff (dataframe): dataframe that stores which stocks are unlisted and newly listed
        """
        # stocks only in latest stock list
        new = diff[diff['_merge']=='right_only']

        try:
            for i in new.to_numpy():
                query = f'INSERT INTO {self.table_name} VALUES(%s, %s)'
                self.cursor.execute(query, (i[0], i[1]))
            
            self.connection.commit()
            
        except Exception as e:
            print(e)

    def __del__(self):
        """close database connection
        """
        self.connection.close()