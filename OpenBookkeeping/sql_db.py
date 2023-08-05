import sqlite3
from loguru import logger
from OpenBookkeeping.gloab_info import create_prop_detail_table, \
    create_prop_table


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


def add_prop(database: str,
             name: str):
    """
    新增一个账户,如果
    :param database: 数据库路经
    :param name: 账户名称
    :return: bool, exist name
    """
    if name == '':
        logger.warning(f'name empty {name=}')
        return False

    with Connect(database) as db:
        sql_str = f"select * from prop where name = ?"
        db.cur.execute(sql_str, (name,), )
        records = db.cur.fetchall()
        if len(records) > 0:
            logger.warning(f'{records}')
            return True

        sql_str = "INSERT INTO prop " \
                  "(name, type, start_date, term_month, rate, currency, ctype, comment)" \
                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        data = (name, 0, '2023-06-01', 0, 0, 0, 0, '')
        db.cur.execute(sql_str, data)
        db.conn.commit()
    return False


def add_detail(database: str,
               target_id: int,
               occur_date: str,
               amount: int,
               notes: str):
    with Connect(database) as db:
        sql_str = f"INSERT INTO  prop_details" \
                  "(target_id, occur_date, amount, notes)" \
                  "VALUES (?, ?, ?, ?)"
        data = (target_id, occur_date, amount, notes)
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


def query_by_col(database: str, table_name: str, col_name: str, col_value: str):
    """
    按一列作为条件，查询数据库中的数据
    :param database: 数据库路径
    :param table_name: 表名称
    :param col_name: 条件列名称
    :param col_value: 条件列的值
    :return: 满足条件的数据条目
    """
    with Connect(database) as db:
        sql_str = f"select * from {table_name} where {col_name} = ?"
        logger.debug(f'{sql_str=}, {col_value=}')
        db.cur.execute(sql_str, (col_value,),)
        records = db.cur.fetchall()
    return records


def del_by_col(database:str, table_name: str, col_name: str, col_value: str):
    with Connect(database) as db:
        sql_str = f'DELETE FROM {table_name} WHERE {col_name} = ?'
        logger.debug(f'{sql_str=}, {col_value=}')
        db.cur.execute(sql_str, (col_value,),)
        db.conn.commit()


def update_by_col(database: str, table_name: str, col_name: str, col_value: str, values: dict):
    """
    以一列为条件，更新数据库中的数据
    :param database: 数据库路径
    :param table_name: 表名称
    :param col_name: 条件列名称
    :param col_value: 条件列的值
    :param values: 数据库中列名称与值
    :return:
    """
    with Connect(database) as db:
        set_strs = [f'{k} = ?' for k in values.keys()]
        set_str = ' , '.join(set_strs)
        vals = list(values.values())
        vals.append(col_value)

        sql_str = f"UPDATE {table_name} SET {set_str} where {col_name} = ?"
        logger.debug(sql_str)
        db.cur.execute(sql_str, tuple(vals),)
        db.conn.commit()


def query_by_str(database: str, sql_str: str):
    logger.debug(f'{sql_str=}')
    with Connect(database) as db:
        db.cur.execute(sql_str,)
        records = db.cur.fetchall()
    return records


def init_db(data_base: str):
    with Connect(database=data_base) as db:
        db.cur.execute(create_prop_table)
        db.cur.execute(create_prop_detail_table)
        db.conn.commit()


if __name__ == "__main__":
    init_db('t.db')
