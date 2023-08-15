# -*- coding: utf-8 -*-
import redis


class RedisUtils:
    """
    RedisUtils 基于 redis 库进行封装
    """

    def __init__(self, host, port, dbnum, password):
        self.redis = redis.Redis(host=host, port=port, db=dbnum, password=password)

    def enqueue_message(self, stream_name, data):
        """向Redis流插入数据

        Args:
            stream_name(str): 流名称
            data(*):数据

        """
        self.redis.xadd(stream_name, data)

    def close(self):
        self.redis.close()
