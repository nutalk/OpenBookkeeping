import sqlite3
from dbutils.persistent_db import PersistentDB
import time


class Pool(object):
    __pool = None

    def __new__(cls, database: str, *args, **kwargs):
        if cls.__pool is None:
            cls.__pool = PersistentDB(sqlite3, maxusage=None,
                                      closeable=False,
                                      database=database)
            return cls.__pool


class Connect:
    def __init__(self, database: str):
        self.database = database

    def __enter__(self):
        db_pool = Pool(database=self.database)
        self.conn = db_pool.connection()
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()


def add_prop(database: str,
             name: str,
             types: int,
             currency: int,
             comment: str):
    current_date = time.time()
    current_date = round(current_date * 1000)
    with Connect(database) as db:
        sql_str = "INSERT INTO prop " \
                  "(name, type, create_date, currency, comment)" \
                  "VALUES (?, ?, ?, ?, ?)"
        data = (name, types, current_date, currency, comment)
        db.cur.execute(sql_str, data)
        db.conn.commit()


def init_db(data_base: str):
    create_prop_table = """
    CREATE TABLE "prop" (
        "id"	INTEGER NOT NULL,
        "name"	text NOT NULL,
        "type"	INTEGER NOT NULL,
        "create_date"	INTEGER NOT NULL,
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
        "create_date"	INTEGER NOT NULL,
        "term_month"	INTEGER NOT NULL,
        "rate"	float NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    )
    """

    create_detail_table = """
    CREATE TABLE "details" (
        "id"	INTEGER NOT NULL,
        "prop_id"	INTEGER NOT NULL,
        "occur_date"	INTEGER NOT NULL,
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

        sql_str = "INSERT INTO prop " \
                  "(name, type, create_date, currency, comment)" \
                  "VALUES (?, ?, ?, ?, ?)"
        data = ('test', 0, 0, 200, 'test_comment')
        db.cur.execute(sql_str, data)
        db.conn.commit()


if __name__ == "__main__":
    init_db('t.db')
