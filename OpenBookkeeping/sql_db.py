import sqlite3
from dbutils.persistent_db import PersistentDB


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


def init_db(data_base: str):
    create_prop_table = """
    CREATE TABLE "prop" (
        "id"	int NOT NULL,
        "name"	text NOT NULL,
        "type"	int NOT NULL,
        "currency_type"	int NOT NULL,
        "create_date"	INTEGER NOT NULL,
        "rate"	float NOT NULL,
        "currency"	int NOT NULL,
        PRIMARY KEY("create_date" AUTOINCREMENT)
    );
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


if __name__ == "__main__":
    init_db('t.db')
