# -*- coding: utf-8 -*-
from liangutil.liangutils import *
from liangutil.mysqlutils import MySQLUtils


class LiangLog:
    def __init__(self, name, is_print_console=True,is_record_file=False,is_record_db=False, dir_path=None, db_host=None, db_port=None, db_user=None, db_pass=None, db_name=None):
        # name 程序名称
        self.name = name

        # is_print_console 是否打印到控制台
        # is_record_file 是否记录到文件中
        # is_record_db 是否记录到mysql中
        self.is_print_console = is_print_console
        self.is_record_file = is_record_file
        self.is_record_db = is_record_db

        # file_path 如果记录到文件，文件放在哪个目录
        self.dir_path = dir_path

        if is_record_file == True:
            check_path(dir_path)

        if is_record_db == True:
            # 检查数据库连接
            # 前提：保证数据库中，有一个名为program_logs表
            # 字段名          类型      长度
            # datetime       varchar  32
            # level          varchar  32
            # name           varchar  32
            # content        varchar  255
            self.mysql = MySQLUtils(db_host, db_port, db_user, db_pass, db_name)

            if self.mysql.check_table_exist("program_logs") == False:
                raise Exception("program_logs 数据表不存在")


    # level等级：WARNING, INFO , ERROR
    # content输出内容
    def print_log(self, level, content):
        formatted_log = "{} EXCEPTION: {}".format(code_location(depth=-4),content)
        log = "{} {} {}".format(level,get_nowdatetime(),formatted_log)
        print(log)


    # 将日志输出到文件
    def record_log_to_file(self,level, content):
        now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        file_path = os.path.join(self.dir_path, self.name + "_logs", get_nowdate(now), level+get_nowtime(now)+".log")
        check_path(file_path)
        with open(file_path, "a", encoding="utf-8") as f:
            formatted_log = "{} EXCEPTION: {}".format(code_location(depth=-4), content)
            log = "{} {} {}".format(level, get_nowdatetime(), formatted_log)
            f.write(log+"\n")


    def record_log_to_db(self, level, content):
        now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        formatted_log = "{} EXCEPTION: {}".format(code_location(depth=-4), content)
        self.mysql.insert_data("program_logs", {"datetime":get_nowdatetime(), "level":level, "name":self.name, "content":formatted_log})


    # 推荐调用这个方法
    def record_log(self, level, content):
        if self.is_print_console:
            self.print_log(level, content)
        if self.is_record_file:
            self.record_log_to_file(level, content)
        if self.is_record_db:
            self.record_log_to_db(level, content)
