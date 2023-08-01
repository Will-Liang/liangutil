# -*- coding: utf-8 -*-
import redis


class RedisUtils:
    def __init__(self, host, port, dbnum, password):
        self.redis = redis.Redis(host=host, port=port, db=dbnum, password=password)


    # 发布消息到 Stream 队列
    def enqueue_message(self, message):
        stream_name = 'minio_file_queue'
        self.redis.xadd(stream_name, {'path': message})
        # print(f"入队信息： {path}")
        # 关闭
        self.redis.close()
