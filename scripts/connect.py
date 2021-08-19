import yaml
from scripts.database import Database


def connect_db() -> Database:
    with open('config/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    user = config['user']['user']
    mysql_pw = config['user']['mysql_password']
    host = config['user']['host']
    db_name = 'us_stock'
    table_name = 'stock_list'

    try:
        db = Database(user, mysql_pw, host, db_name, table_name)
        return db
    except Exception as e:
        print(e)
