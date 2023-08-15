# -*- coding: utf-8 -*-
import datetime
import json
import os
import random
import re
import time
import traceback
import tarfile
import zipfile
import rarfile
import gzip
import shutil
import pytz

"""
liangutils 中存放一些工具方法
"""


def is_filepath(path):
    """判断是否为文件路径

    相对路径不要使用 ./ 开头

    Args:
        path: 路径

    Returns:
        bool: 包含文件名称的路径返回 True，否则返回 False

    '"""
    pattern = r'\.[a-zA-Z]+$'  # 匹配以.开头，后面跟着至少一个字符的字符串
    return bool(re.search(pattern, path))


def get_dirpath(path):
    """获得目录路径

    如果是文件路径，提取父级目录路径（相对路径不要使用 ./ 开头）

    Args:
        path: 路径

    Returns:
        str: 目录路径

    """
    # 是文件路径，需要提取父级目录路径
    if is_filepath(path):
        # 获取当前操作系统的文件目录分隔符
        separator = os.sep

        # 有父级目录
        if str(path).rfind(".") != -1 and str(path).rfind(separator) != -1:
            return str(path).rsplit(separator, 1)[0]
        elif str(path).rfind(".") != -1:
            # 类似 a.txt
            return ""
        else:
            return ""
    else:
        return path


def check_path(path):
    """检查目录是否存在

    如果目录不存在创建目录

    Args:
        path: 路径

    Returns:
        str: 路径

    """
    dirpath = get_dirpath(path)
    if dirpath != "" and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return path


def print_log(level, content):
    """打印日志

    Args:
        level: 日志等级
        content: 信息

    """
    formatted_log = "{} EXCEPTION: {}".format(code_location(depth=-3), content)
    printlog = "{} {} {}".format(level, get_nowdatetime(), formatted_log)
    print(printlog)


def code_location(depth=-2):
    """得到调用该方法的文件名称和 代码行号

    Args:
        depth: 如果直接得到调用该方法的代码在哪里，传递-2

    Returns:
        str: {调用该方法的pytho文件名} line {行号}
    """
    stack = traceback.extract_stack()
    filename, lineno, _, _ = stack[depth]
    # 在 Python 中，traceback.extract_stack() 函数返回当前的调用栈信息。调用栈是一个包含多个元组的列表，每个元组表示一帧（frame）的信息。每一帧都对应着一次函数调用，包含了函数所在的文件名、行号、函数名等信息。
    # 通常，调用栈列表的最后一帧是当前代码所在的位置，也就是 code_location() 函数本身的位置。而在 traceback.extract_stack() 返回的列表中，最后一帧的索引是 -1。而倒数第二帧的索引是 -2，依此类推。
    # 所以在代码中的 stack[-2] 就表示获取调用栈列表中倒数第二帧的信息，即 code_location() 函数被调用的位置所在的帧。然后从这个帧中获取文件名和行号信息，最终返回文件名和行号组成的字符串。
    # 注意：traceback.extract_stack() 函数会返回完整的调用栈信息，包含当前函数的调用。如果你在其他函数中调用了 code_location()，那么它返回的文件名和行号将是调用它的位置。
    return filename + " line:" + str(lineno)


def get_nowdatetime():
    """获得亚洲上海时区现在的日期时间

    Returns:
        str: 时间字符串

    """
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    current_date = now.strftime('%Y-%m-%d')  # 2023-04-17
    current_hour = now.strftime('%H')
    current_min = now.strftime('%M')
    current_sec = now.strftime('%S')
    nowdatetime = (
        current_date + " " + current_hour + ":" + current_min + ":" + current_sec
    )
    return nowdatetime


def get_nowtime(now):
    """获得现在的时间

    Args:
        now: now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))

    Returns:
        str: 时间字符串

    """
    current_hour = now.strftime('%H')
    current_min = now.strftime('%M')
    current_sec = now.strftime('%S')
    time = current_hour + ":" + current_min + ":" + current_sec
    return time


def get_nowdate(now):
    """获得现在的日期

    Args:
        now: now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))

    Returns:
        str: 日期字符串

    """
    current_date = now.strftime('%Y-%m-%d')  # 2023-04-17
    return current_date


def uncompress(src_file, dest_dir_path):
    """解压文件(支持zip,tgz,tar,rar,gz)

    Args:
        src_file(str): 压缩包
        dest_dir_path(str): 解压的目录

    Returns:
        bool: True/False
    """
    try:
        print(get_nowdatetime() + "starting uncompress: " + src_file)
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
        if src_file.endswith('.tgz') or src_file.endswith('.tar'):
            tar = tarfile.open(src_file)
            for name in tar.getnames():
                tar.extract(name, dest_dir_path)
            tar.close()
        elif src_file.endswith('.zip'):
            zip_file = zipfile.ZipFile(src_file)
            for names in zip_file.namelist():
                zip_file.extract(names, dest_dir_path)
            zip_file.close()
        elif src_file.endswith('.rar'):
            rar = rarfile.RarFile(src_file)
            rar.extractall(dest_dir_path)
            rar.close()
        elif src_file.endswith('.gz'):
            '''
            g_file = gzip.GzipFile(src_file)# 创建gzip对象
            with open(os.path.join(dest_dir_path, os.path.basename(src_file).split(".gz")[0]), "wb") as f:
                f.write(g_file.read()) # gzip对象用read()打开后，写入open()建立的文件中。
            g_file.close()  # 关闭gzip对象
            '''
            with gzip.open(src_file, 'rb') as s_file, open(
                os.path.join(dest_dir_path, os.path.basename(src_file).split(".gz")[0]),
                'wb',
            ) as d_file:
                shutil.copyfileobj(s_file, d_file, 65536)
        else:
            print("Incorrect file type")
            return False
        print(get_nowdatetime() + ": success uncompress: " + src_file)
    except Exception as e:
        print(str(e))
        return False
    return True


def find_all_files(directory):
    """根据目录寻找该目录下的所有子文件

    Args:
        directory(str):目录路径

    Returns:
        list: 子文件路径
    """
    file_paths = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    return file_paths


def random_sleep(lower_bound: int, upper_bound: int):
    """随机睡眠若干秒

    Args:
        lower_bound(int):最少睡眠秒数
        upper_bound(int):最多睡眠秒数

    """
    random_sleep_time = random.uniform(lower_bound, upper_bound)
    print(f"随机等待时间：{random_sleep_time:.2f}秒")
    time.sleep(random_sleep_time)
    print("随机等待时间结束")


def file_to_json(file_path, encoding="utf-8"):
    """读取json文件

    Args:
        file_path(str): 文件路径
        encoding(str): 编码格式

    Returns:
        dict: 正确情况

    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return json.load(f)
    except Exception as e:
        print(repr(e))
        return None


def file_to_json_line(file_path, encoding="utf-8"):
    """逐行读取每行都是json的文件

    Args:
        file_path(str): 文件路径
        encoding(str): 编码格式

    Returns:
        list: [{},{},{}]
    """
    try:
        all_line = []
        with open(file_path, "r", encoding=encoding) as f:
            for line in f.readlines():
                if line:
                    try:
                        all_line.append(json.loads(line.strip()))
                    except Exception as e:
                        print(repr(e))
        return all_line
    except Exception as e:
        print(repr(e))
        return None


def json_to_line_file(outputfile, all_line, encoding="utf-8"):
    """将一个列表中的每个dict逐行写入文件

    Args:
        outputfile(str):输出文件路径
        all_line(list):存储dict的list
        encoding(str):编码格式

    Returns:
        bool: True/False
    """
    try:
        with open(outputfile, "w", encoding=encoding) as f_output:
            for ip in all_line:
                try:
                    f_output.writelines(json.dumps(ip) + "\n")
                except Exception as e:
                    print(repr(e))
        print("json_to_line_file(): " + outputfile + ", is OK!")
        return True
    except Exception as e:
        print(repr(e))
        return False


def json_to_file(outputfile, json_data, encoding="utf-8"):
    """将json写入文件

    Args:
        outputfile(str):输出文件路径
        json_data(dict):json数据
        encoding(str):编码格式

    Returns:
        bool: True/False
    """
    try:
        with open(outputfile, "w", encoding=encoding) as f:
            json.dump(json_data, f)
        print("json_to_file: " + outputfile + ", is OK!")
        return True
    except Exception as e:
        print(repr(e))
        return False


def json_to_file_format(outputfile, json_data, encoding="utf-8"):
    """将json格式化写入文件

    Args:
        outputfile(str):输出文件路径
        json_data(dict):json数据
        encoding(str):编码格式

    Returns:
        bool: True/False
    """
    try:
        with open(outputfile, "w", encoding=encoding) as f:
            json.dump(json_data, f, sort_keys=True, ensure_ascii=False, indent=2)
        print("json_to_file_format: " + outputfile + ", is OK!")
        return True
    except Exception as e:
        print(repr(e))
        return False


