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

    def check_table_exists(self):
        """check if stock list is already in the database

        Returns:
            int: 0 for empty, 1 for exists
        """
        query ='SHOW TABLES LIKE \'us_stock\''
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        # check if the length is 0, which means there's no table
        if len(res) == 0:
            return 0
        else:
            return 1

    def save_in_db(self, stock_list, table_name):
        """save received stock list in a database table

        Args:
            stock_list (dataframe): latest list of stock listed in US
            table_name (string): table name to save as
        """
        try:
            stock_list.to_sql(table_name, self.engine, index=False)
            print('Successfully added to database.')
        except Exception as e:
            print(e)

    def read_db(self):
        """get stock list saved in the database

        Returns:
            dataframe: stock list saved in the database
        """
        try:
            stock_list = pd.read_sql_table('us_stock', self.engine)
            return stock_list
        except Exception as e:
            print(e)

    def delete_stock(self, table_name, diff):
        """delete stocks from stock list database which are unlisted from stock exchange

        Args:
            table_name (string): database table name to delete from
            diff (dataframe): dataframe that stores which stocks are unlisted and newly listed
        """
        # stocks only in past stock list
        old = diff[diff['_merge']=='left_only']
        
        # delete stock from stock list
        try:
            for i in old['Symbol']:
               query = 'DELETE FROM '+table_name+' WHERE Symbol=%s'
               self.cursor.execute(query, i)

            self.connection.commit()

        except Exception as e:
            print(e)

    def add_stock(self, table_name, diff):
        """add stocks to stock list database wihch are newly listed in stock exchange

        Args:
            table_name (string): database table name to add in
            diff (dataframe): dataframe that stores which stocks are unlisted and newly listed
        """
        # stocks only in latest stock list
        new = diff[diff['_merge']=='right_only']

        # add new stock list
        try:
            for i in new.to_numpy():
                query = 'INSERT INTO '+table_name+' VALUES(%s, %s, %s)'
                self.cursor.execute(query, (i[0], i[1], i[2]))
            
            self.connection.commit()
            
        except Exception as e:
            print(e)

    def __del__(self):
        """close database connection
        """
        self.connection.close()