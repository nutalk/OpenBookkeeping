import sqlite3
import time
from loguru import logger


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
    cols_str = ' '.join(cols)
    with Connect(database) as db:
        sql_str = f"""select {cols_str} from {table_name}"""
        logger.debug(f'{sql_str=}')
        db.cur.execute(sql_str)
        records = db.cur.fetchall()
    return records


def init_db(data_base: str):
    create_prop_table = """
    CREATE TABLE "prop" (
        "id"	INTEGER NOT NULL,
        "name"	text NOT NULL,
        "type"	INTEGER NOT NULL,
        "start_date"	text NOT NULL,
        "currency"	INTEGER NOT NULL,
        "comment" text,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """

    create_liability_table = """
    CREATE TABLE "liability" (
        "id"	INTEGER NOT NULL,
        "name"	TEXT NOT NULL,
        "type"	INTEGER NOT NULL,
        "currency_type"	INTEGER NOT NULL,
        "start_date" text NOT NULL,
        "term_month"	INTEGER NOT NULL,
        "rate"	float NOT NULL,
        "comment" text,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """

    create_detail_table = """
    CREATE TABLE "details" (
        "id"	INTEGER NOT NULL,
        "prop_id"	INTEGER NOT NULL,
        "occur_date"	text NOT NULL,
        "amount"	INTEGER NOT NULL,
        "notes"	TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
    );
    """

    with Connect(database=data_base) as db:
        db.cur.execute(create_prop_table)
        db.conn.commit()
        db.cur.execute(create_detail_table)
        db.conn.commit()
        db.cur.execute(create_liability_table)
        db.conn.commit()


if __name__ == "__main__":
    init_db('t.db')
