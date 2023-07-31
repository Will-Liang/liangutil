import datetime
import os
import re
import traceback

import pytz


# 判断是否为文件路径
# 相对路径不要使用 ./ 开头
def is_filepath(path):
    pattern = r'\.[a-zA-Z]+$'  # 匹配以.开头，后面跟着至少一个字符的字符串
    return bool(re.search(pattern, path))

# 如果是文件路径，提取父级目录路径
# 相对路径不要使用 ./ 开头
def get_dirpath(path):
    # 是文件路径，需要提取父级目录路径
    if is_filepath(path):
        # 有父级目录
        if str(path).rfind(".") != -1 and str(path).rfind("/") != -1:
            return str(path).rsplit("/", 1)[0]
        elif str(path).rfind(".") != -1:
            # 类似 a.txt
            return ""
        else:
            return ""
    else:
        return path


# 检查目录是否存在
def check_path(path):
    dirpath = get_dirpath(path)
    if dirpath != "" and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return path


# 打印日志
def print_log(level, content):
    formatted_log = "{} EXCEPTION: {}".format(code_location(depth=-2), content)
    printlog = "{} {} {}".format(level,get_nowdatetime(),formatted_log)
    print(printlog)



# 得到调用该方法的文件名称和 代码行号
# depth: 如果直接得到调用该方法的代码在哪里，传递-2
def code_location(depth=-2):
  stack = traceback.extract_stack()
  filename, lineno, _, _ = stack[depth]
  # 在 Python 中，traceback.extract_stack() 函数返回当前的调用栈信息。调用栈是一个包含多个元组的列表，每个元组表示一帧（frame）的信息。每一帧都对应着一次函数调用，包含了函数所在的文件名、行号、函数名等信息。
  # 通常，调用栈列表的最后一帧是当前代码所在的位置，也就是 code_location() 函数本身的位置。而在 traceback.extract_stack() 返回的列表中，最后一帧的索引是 -1。而倒数第二帧的索引是 -2，依此类推。
  # 所以在代码中的 stack[-2] 就表示获取调用栈列表中倒数第二帧的信息，即 code_location() 函数被调用的位置所在的帧。然后从这个帧中获取文件名和行号信息，最终返回文件名和行号组成的字符串。
  # 注意：traceback.extract_stack() 函数会返回完整的调用栈信息，包含当前函数的调用。如果你在其他函数中调用了 code_location()，那么它返回的文件名和行号将是调用它的位置。
  return filename+" line:"+str(lineno)


# 获得现在的日期时间
def get_nowdatetime():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    current_date = now.strftime('%Y-%m-%d')  # 2023-04-17
    current_hour = now.strftime('%H')
    current_min = now.strftime('%M')
    current_sec = now.strftime('%S')
    nowdatetime = current_date + " " + current_hour + ":" + current_min + ":" + current_sec
    return nowdatetime


# 获得现在的时间
# now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
def get_nowtime(now):
    current_hour = now.strftime('%H')
    current_min = now.strftime('%M')
    current_sec = now.strftime('%S')
    time = current_hour + ":" + current_min + ":" + current_sec
    return time


# 获得现在的日期
# now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
def get_nowdate(now):
    current_date = now.strftime('%Y-%m-%d')  # 2023-04-17
    return current_date


