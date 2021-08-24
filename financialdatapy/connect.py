import yaml
from financialdatapy.database import Database


def connect_db() -> Database:
    with open('config/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    rdb = 'mysql'
    dbapi = 'pymysql'
    user = config['user']['user']
    mysql_pw = config['user']['mysql_password']
    host = config['user']['host']
    db = 'us_stock'
    table = 'stock_list'

    try:
        db = Database(rdb, dbapi,
                      user, mysql_pw, host,
                      db, table)
    except Exception as e:
        print(e)
    else:
        return db
