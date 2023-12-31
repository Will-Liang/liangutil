# -*- coding: utf-8 -*-
import pymysql

class MySQLUtils:
    """
    MySQLUtils 基于 pymysql 库进行封装
    """

    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(
            host=host, port=port, user=username, password=password, database=database
        )

    def check_table_exist(self, table_name):
        """根据表名检查表是否存在

        Args:
            table_name(str):表名

        Returns:
            存在返回True，否则返回False

        """
        cursor = self.conn.cursor()

        sql = "show tables like '{}'".format(table_name)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    def insert_data(self, table_name, data: dict):
        """插入一条数据

        Args:
            table_name(str):表名
            data(dict):要插入的数据，以字段名为键，字段值为值。

        Returns:
            插入成功返回"True"

        """
        cursor = self.conn.cursor()
        # 构建 SQL 插入语句
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"insert into {table_name} ({columns}) values ({values})"
        cursor.execute(sql, tuple(data.values()))
        self.conn.commit()
        cursor.close()
        return "True"

    def insert_datas(self, table_name, data_list: list):
        """插入一条数据

        Args:
            table_name(str):表名
            data(list):要插入的数据列表，以字段名为键，字段值为值。

        Returns:
            插入成功返回"True"

        """

        cursor = self.conn.cursor()
        columns = ', '.join(data_list[0].keys())  # 假设所有字典的键相同
        values_template = ', '.join(['%s'] * len(data_list[0]))
        # 构建 SQL 批量插入语句
        sql = f"insert into {table_name} ({columns}) values ({values_template})"
        # 构建数据列表的值元组
        values_tuples = [tuple(d.values()) for d in data_list]
        cursor.executemany(sql, values_tuples)
        self.conn.commit()
        cursor.close()
        return "True"

    def query_data(self, table_name, columns=[], condition=None):
        """随机查询单条数据

        Args:
            table_name(str):表名
            columns(list): 要查询的列名列表，如果为[]，则查询所有列
            condition(str): 查询条件

        Returns:
            查询结果

        """
        cursor = self.conn.cursor()
        if len(columns) == 0:
            columns_str = "*"
        else:
            columns_str = ', '.join(columns)
        sql = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition} order by rand() limit 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def query_datas(self, table_name, columns=None, condition=None):
        """查询数据

        Args:
            table_name(str):表名
            columns(list): 要查询的列名列表，如果为[]，则查询所有列
            condition(str): 查询条件

        Returns:
            查询结果(元组)，每条记录为一个元组

        """
        cursor = self.conn.cursor()
        if columns is None:
            columns = []
        columns_str = "*" if len(columns) == 0 else ', '.join(columns)
        sql = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query_datas_dict_list(self, table_name, columns=None, condition=None):
        """查询数据

        Args:
            table_name(str):表名
            columns(list): 要查询的列名列表，如果为[]，则查询所有列
            condition(str): 查询条件

        Returns:
            查询结果 [{},{},{}]

        """
        cursor = self.conn.cursor()
        if columns is None:
            columns = []
        columns_str = "*" if len(columns) == 0 else ', '.join(columns)
        sql = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        cursor.execute(sql)
        result = self.fetchall_to_dict_list(cursor)
        cursor.close()
        return result

    def exists_data(self, table_name, columns=None, condition=None):
        """是否存在该数据

        Args:
            table_name(str):表名
            columns(list): 要查询的列名列表，如果为[]，则查询所有列
            condition(str): 查询条件

        Returns:
            存在True，否则False

        """
        if columns is None:
            columns = []
        if condition is None:
            print(
                "WARNING",
                " You didn't pass in a condition parameter, so it's pointless",
            )
        datas = self.query_data(table_name, columns, condition)
        if datas != None:
            return len(datas) > 0
        return False

    def update_datas(self, table_name, data, condition=None):
        """更新数据

        Args:
            table_name(str): 表名
            data(dict): 要更新的数据，以字段名为键，字段值为值。
            condition(str): 更新条件

        Returns:
            更新成功返回 "True"，失败返回异常
        """
        cursor = self.conn.cursor()
        # 构建 SQL 更新语句
        set_columns = ', '.join([f"{column} = %s" for column in data.keys()])
        sql = f"UPDATE {table_name} SET {set_columns}"
        if condition:
            sql += f" WHERE {condition}"
        # 执行 SQL 更新
        cursor.execute(sql, tuple(data.values()))
        # 提交事务
        self.conn.commit()
        cursor.close()
        return "True"

    def fetchall_to_dict_list(self, cursor):
        """将pymysql的fetchall查询结果转换为装有dict类型的列表

        Args:
            cursor: pymysql游标对象

        Returns:
            装有字典类型的列表
        """
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in cursor.fetchall()]

