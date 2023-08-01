# liangutil包

![Python](https://img.shields.io/badge/python-3.x-blue.svg)   ![PyPI](https://img.shields.io/pypi/v/liangutil)   ![PyPI - Downloads](https://img.shields.io/pypi/dd/liangutil)   ![GitHub stars](https://img.shields.io/github/stars/Will-Liang/liangutil.svg)

**说明：以Liang开头的类是单独写的类，以Utils结尾的都是基于第三方库封装的。函数详细说明请看代码注释。**

**安装**

```
pip install liangutil
```



## liangutils

函数列表：

- **is_filepath(path)**：判断路径是否为文件路径
- **get_dirpath(path)**：根据文件路径获得其父级目录路径
- **check_path(path)**：检查路径是否存在
- **print_log(level, content)**：打印日志
- **code_location(depth=-2)**：获得调用该方法的函数在哪里
- **get_nowdatetime()**：获得现在的日期时间
- **get_nowtime(now)**：获得现在的时间
- **get_nowdate(now)**：获得现在的日期



## requestutils

### RequestUtils

**基于Requests库的封装**

函数列表：

- **get_header(self, is_choice_agent=False)**：获得请求头
- **get(self, url, header="", retry_count=3, is_response_json=False, time_sleep=1, proxy=None)**：Get请求



## mysqlutils

### **MySQLUtils**

**基于pymysql库的封装**

函数列表：

- **check_table_exist(self, table_name)**：根据表名检查表是否存在
- **insert_data(self, table_name, data: dict)**：向数据表插入一条记录
- **insert_datas(self, table_name, data_list: list)**：向数据表中插入多条记录



## lianglog

### LiangLog

依赖于 **MySQLUtils**

函数列表：

- **print_log(self, level, content)**：打印日志到控制台
- **record_log_to_file(self,level, content)**：将日志输出到文件
- **record_log_to_db(self, level, content)**：将日志输出到mysql数据库中
- **record_log(self, level, content)**：记录日志总方法



| 字段名   | 类型    | 长度 |
| -------- | ------- | ---- |
| datetime | varchar | 32   |
| level    | varchar | 32   |
| name     | varchar | 32   |
| content  | varchar | 255  |



## redisutils

### RedisUtils

**基于redis库的封装**

函数列表：

- **enqueue_message(self, message)**：向redis插入条数据



## minioutils

### MinIOUtils

**基于minio库的封装**，依赖于 **RedisUtils**

函数列表

- **get_configfile(self)**：读取配置文件
- **upload_file_to_minio(self, bucket_name: str, file_path: str, current_path: str)**：将文件上传至MinIO
- **upload_file_to_minio_notify(self, bucket_name: str, file_path: str, current_path: str)**：将文件上传至MinIO，并向Redis通知



# 更新日志

## 2023年

### 8月



**2023-08-01** `0.1.1`

- 统一了代码注释风格

- mysqlutils 中增加了查询等方法
- 修复了一些 Bug

### 7月

**2023-07-31** `0.0.8`

- 第一个发布版本

