from sqlalchemy import create_engine, inspect
import pymysql
import pandas as pd


class Database:
    def __init__(self, user: str, mysql_pw: str,
                 host: str, db_name: str, table_name: str) -> None:
        """connect to a mysql server

        Args:
            user (string): mysql username
            mysql_pw (string): mysql password
            host (string): mysql host
            db_name (string): database name to work in
            table_name (string): table name to work in
        """
        self.user = user
        self.mysql_pw = mysql_pw
        self.host = host
        self.db_name = db_name
        self.table_name = table_name

        self.engine = create_engine(
            f'mysql+mysqldb://{self.user}:{self.mysql_pw}@{self.host}/',
            encoding='utf-8',
        )
        self.insp = inspect(self.engine)

        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.mysql_pw,
        )
        self.cursor = self.connection.cursor()

        query = f'CREATE DATABASE IF NOT EXISTS {self.db_name}'
        self.cursor.execute(query)

        query = f'USE {self.db_name}'
        self.cursor.execute(query)

        self.connection.commit()

    def save_in_db(self, latest_stock_list: pd.DataFrame) -> None:
        """save latest stock list in database

        stocks that are not in the latest stock list
        will have 'left_only' value whereas new stocks
        will have 'right_only' value under '_merge' column

        Args:
            latest_stock_list (dataframe): latest stock list
        """
        check = self.insp.has_table(self.table_name, self.db_name)

        if check:
            old_stock_list = self.read_table()
            merged = pd.merge(
                old_stock_list,
                latest_stock_list,
                how='outer',
                indicator=True,
            )
            diff = merged[merged['_merge'] != 'both']

            if not diff.empty:
                self.delete_stock(diff)
                self.add_stock(diff)
        else:
            latest_stock_list.to_sql(
                self.table_name,
                self.engine,
                self.db_name,
                index=False,
            )

    def read_table(self) -> pd.DataFrame:
        """get stock list saved in the database

        Returns:
            dataframe: stock list saved in the database
        """
        stock_list = pd.read_sql_table(
            self.table_name,
            self.engine,
            self.db_name,
        )
        return stock_list

    def delete_stock(self, diff: pd.DataFrame) -> None:
        """Delete stocks from stock list database.

        Retrieve rows which the value in column '_merge' is 'left_only' since
        'left_only' is the ones that are not in the latest stock list. Then
        deletes it from the stock_list database.

        Args:
            diff (dataframe): Dataframe that stores which stocks are
                unlisted and newly listed
        """
        old = diff[diff['_merge'] == 'left_only']

        try:
            for i in old['Symbol']:
                query = f'DELETE FROM {self.table_name} WHERE ticker=%s'
                self.cursor.execute(query, i)

            self.connection.commit()

        except pymysql.ProgrammingError as e:
            print(e)

    def add_stock(self, diff: pd.DataFrame) -> None:
        """add stocks to stock list database.

        Args:
            diff (dataframe): dataframe that stores which stocks
                are unlisted and newly listed
        """
        # stocks only in latest stock list
        new = diff[diff['_merge'] == 'right_only']

        try:
            for i in new.to_numpy():
                query = f'INSERT INTO {self.table_name} VALUES(%s, %s)'
                self.cursor.execute(query, (i[0], i[1]))

            self.connection.commit()

        except pymysql.ProgrammingError as e:
            print(e)

    def __del__(self) -> None:
        """close database connection
        """
        self.connection.close()
