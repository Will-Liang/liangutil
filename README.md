# liangutil包

![Python](https://img.shields.io/badge/python-3.x-blue.svg)   ![PyPI](https://img.shields.io/pypi/v/liangutil)   ![PyPI - Downloads](https://img.shields.io/pypi/dm/liangutil)   ![GitHub stars](https://img.shields.io/github/stars/Will-Liang/liangutil.svg)

**说明：以Liang开头的类是单独写的类，以Utils结尾的都是基于第三方库封装的。函数详细说明请看代码注释。**

**文档**：https://will-liang.github.io/liangutil/

## **安装**

```
pip install liangutil
```



## 说明

### liangutils

存放一些工具函数



### requestutils

#### RequestUtils

基于Requests库的封装

#### ChromeUtils

基于selenium库的封装



### mysqlutils

#### **MySQLUtils**

基于pymysql库的封装



### lianglog

#### LiangLog

依赖于 **MySQLUtils**

需要在mysql中建立表，字段如下

| 字段名   | 类型    | 长度 |
| -------- | ------- | ---- |
| datetime | varchar | 32   |
| level    | varchar | 32   |
| name     | varchar | 32   |
| content  | varchar | 255  |



### redisutils

#### RedisUtils

基于redis库的封装



### minioutils

#### MinIOUtils

基于minio库的封装



# 更新日志

## 2023年

### 8月

**2023-08-10**

`0.1.6`

- RequestUtils的 `__init__`增加了`proxy_host`参数
- RequestUtils中增加了用于下载文件、克隆代码仓库等方法
- liangutils中增加了uncompress()用于解压文件

**2023-08-09**

`0.1.5`

- ChromeUtils中get_page_source()可以使用代理了，重试机制只适用于网页源码返回为 `<html><head></head><body></body></html>` 情况
- 修复了一些Bug

**2023-08-04**

`0.1.4`

- ChromeUtils增加隐藏浏览器特征和反屏蔽

**2023-08-03**

`0.1.3`

- 取消了某些函数的捕获异常
- 修复了一些Bug

**2023-08-02** 

`0.1.2`

- 更改了RequestUtils中的get、post方法参数列表名称，更符合使用requests库的习惯
- MySQLUtils增加了 update_datas() 、query_datas_dict_list()

`0.1.1`

- 统一了代码注释风格
- 新增代码文档
- 删除了无用函数
- 改变了某些函数名称

**2023-08-01** 

`0.1.0`

- mysqlutils 中增加了查询等方法
- 修复了一些 Bug

### 7月

**2023-07-31** 

`0.0.8`

- 第一个发布版本

