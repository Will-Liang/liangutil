# liangutil包

![Python](https://img.shields.io/badge/python-3.x-blue.svg)   ![PyPI](https://img.shields.io/pypi/v/liangutil)   ![PyPI - Downloads](https://img.shields.io/pypi/dm/liangutil)   ![GitHub stars](https://img.shields.io/github/stars/Will-Liang/liangutil.svg)

**说明：以Liang开头的类是单独写的类，以Utils结尾的都是基于第三方库封装的。函数详细说明请看代码注释。**

## **安装**

```
pip install liangutil
```



## 注意

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



# 更新日志

## 2023年

### 8月

**2023-08-02** `0.1.1`

- 统一了代码注释风格
- 新增代码文档
- 删除了无用函数

**2023-08-01** `0.1.0`

- mysqlutils 中增加了查询等方法
- 修复了一些 Bug

### 7月

**2023-07-31** `0.0.8`

- 第一个发布版本

