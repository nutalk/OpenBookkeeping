import sqlite3
import time
from loguru import logger
from OpenBookkeeping.gloab_info import create_liability_detail_table, create_prop_detail_table, \
    create_prop_table, create_liability_table

def init_connect(database: str):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    return conn, cursor


class Connect:
    def __init__(self, database: str):
        self.database = database

    def __enter__(self):
        self.conn, self.cur = init_connect(self.database)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()


def add_liability(database: str,
                  name: str, 
                  types: int, 
                  currency_type: int,
                  rate: float,
                  start_date: str, 
                  term_month: int,
                  comment: str ):
    with Connect(database) as db:
        sql_str = "INSERT INTO liability " \
                  "(name, type, currency_type, rate, start_date, term_month, comment)" \
                  "VALUES (?, ?, ?, ?, ?, ?, ?)"
        data = (name, types, currency_type, rate, start_date,term_month, comment)
        db.cur.execute(sql_str, data)
        db.conn.commit()


def add_prop(database: str,
             name: str,
             types: int,
             currency: int,
             start_date: str,
             comment: str):

    with Connect(database) as db:
        sql_str = "INSERT INTO prop " \
                  "(name, type, start_date, currency, comment)" \
                  "VALUES (?, ?, ?, ?, ?)"
        data = (name, types, start_date, currency, comment)
        db.cur.execute(sql_str, data)
        db.conn.commit()


def query_table(database: str, cols: list, table_name: str):
    cols_str = ', '.join(cols)
    with Connect(database) as db:
        sql_str = f"""select {cols_str} from {table_name}"""
        logger.debug(f'{sql_str=}')
        db.cur.execute(sql_str)
        records = db.cur.fetchall()
    return records


def query_detail(database: str, target_id: int, detail_table_name: str):
    with Connect(database) as db:
        sql_str = f"select * from {detail_table_name} where target_id = ?"
        db.cur.execute(sql_str, (target_id,),)
        records = db.cur.fetchall()
    return records


def query_by_str(database: str, sql_str: str):
    with Connect(database) as db:
        db.cur.execute(sql_str,)
        records = db.cur.fetchall()
    return records



def init_db(data_base: str):
    with Connect(database=data_base) as db:
        db.cur.execute(create_prop_table)
        db.cur.execute(create_prop_detail_table)
        db.cur.execute(create_liability_table)
        db.cur.execute(create_liability_detail_table)
        db.conn.commit()



if __name__ == "__main__":
    init_db('t.db')
