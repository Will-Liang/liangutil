# -*- coding: utf-8 -*-
import pymysql

from liangutil.liangutils import print_log


class MySQLUtils:
    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(host=host,port=port, user=username, password=password, database=database)


    # 检查表是否存在
    def check_table_exist(self, table_name):
        cursor = self.conn.cursor()
        try:
            sql = "show tables like '{}'".format(table_name)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False

        except Exception as e:
            print_log("ERROR",e)
        finally:
            cursor.close()


    # 向数据库中插入一条记录
    # 插入成功返回"True"
    def insert_data(self, table_name, data: dict):
        """
        向数据库中插入一条记录
        :param table_name: 表名
        :param data:(dict)要插入的数据，以字段名为键，字段值为值。
        :return:
        """
        try:
            cursor = self.conn.cursor()
            # 构建 SQL 插入语句
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = f"insert into {table_name} ({columns}) values ({values})"

            cursor.execute(sql, tuple(data.values()))

            self.conn.commit()

            cursor.close()
            return "True"
        except Exception as e:
            return e

    # 向数据库中插入多条记录
    # 插入成功返回 "True"
    def insert_datas(self, table_name, data_list: list):
        """
        向数据库中插入多条记录
        :param table_name: 表名
        :param data_list: (list) 要插入的数据列表，每个元素是一个字典，以字段名为键，字段值为值。
        :return: 成功返回 "True"
        """
        try:
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
        except Exception as e:
            return e


    def query_data(self, table_name, columns=[], condition=None):
        """
        查询数据的方法
        :param table_name: 表名
        :param columns: 要查询的列名列表，如果为[]，则查询所有列
        :param condition: 查询条件，可以为 None
        :return: 随机返回一条结果，结果是字典
        """
        try:
            cursor = self.conn.cursor()

            if len(columns) == 0:
                columns_str = "*"
            else:
                columns_str = ', '.join(columns)

            sql = f"SELECT {columns_str} FROM {table_name}"
            if condition:
                sql += f" WHERE {condition} order by rand() limit 1"
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except Exception as e:
            print_log("ERROR", e)
            return None
        finally:
            cursor.close()

    def query_datas(self, table_name, columns=None, condition=None):
        """
        查询数据的方法
        :param table_name: 表名
        :param columns: 要查询的列名列表，如果为[]，则查询所有列
        :param condition: 查询条件，可以为 None
        :return:查询结果元组，每条记录为一个字典
        """
        try:
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
        except Exception as e:
            print_log("ERROR",e)
            return None
        finally:
            cursor.close()

    def exists_data(self, table_name, columns=None, condition=None):
        if columns is None:
            columns = []
        if condition is None:
            print_log("WARNING", "You didn't pass in a condition parameter, so it's pointless")
        datas = self.query_data(table_name, columns, condition)
        if datas != None:
            return len(datas) > 0

