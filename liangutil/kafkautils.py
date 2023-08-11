# -*- coding: utf-8 -*-
from confluent_kafka import Producer, Consumer

from liangutil.liangutils import get_nowdatetime



def kafka_callback(err, msg):
    """kafka的回调函数(不要直接调用)

    """
    if err is not None:
        print("Failed to deliver message: {0} || {1}".format(err, get_nowdatetime()))
    else:
        print("Message produced success in : {0} || {1}".format(msg.topic(), get_nowdatetime()))


def kafka_producer(topic, message, key, broker_ips):
    """向kafka发送消息

    Args:
        topic(str): 将要发送的 Kafka 主题
        message(str): 要发送的消息
        key(str):用于分区的键
        broker_ips(list): Kafka broker IP 地址列表

    """
    # 用逗号分隔 broker_ips 列表以生成 bootstrap.servers 配置值。
    bootstrap_servers = ','.join(broker_ips)

    # 创建 Kafka 配置和生产者实例
    conf = {
        'bootstrap.servers': bootstrap_servers
    }
    p = Producer(conf)
    # 生产并发送消息
    p.produce(topic,value=message.encode('utf-8'), key=key.encode('utf-8'), callback=kafka_callback)
    # 等待未完成的消息，确保所有消息都已发送
    p.flush(timeout=30)


def kafka_consumer(broker_ips, topics, group_id, auto_offset_reset='earliest', timeout=1, message_limit=1):
    """Kafka消费者

    Args:
        broker_ips(list):Kafka broker IP 地址列表
        topics(list):要订阅的 Kafka 主题列表
        group_id(str): 消费者组 ID
        auto_offset_reset(str): 从主题开始的位置消费，可选值为 'earliest' 或 'latest'。
        timeout(int): 消费者轮询超时时间
        message_limit(int): 需要处理的消息数量限制

    Returns:
        dict: 消费者收到的记录列表，每个记录为一个字典，包含 key, value, topic, partition, offset 信息。
    """
    # 定义 Kafka 配置
    conf = {
        'bootstrap.servers': ','.join(broker_ips),
        'group.id': group_id,
        'auto.offset.reset': auto_offset_reset
    }

    # 创建消费者
    consumer = Consumer(conf)

    # 订阅主题
    consumer.subscribe(topics)

    # 定义一个列表，用于保存接收到的消息
    messages = []

    # 持续监听并处理消息，直到达到消息限制
    processed_messages = 0
    while message_limit is None or processed_messages < message_limit:
        msg = consumer.poll(timeout)

        if msg is None:
            # 在这里可以处理没有消息的情况（例如记录或异步处理）
            print("kafka msg is null")
        elif msg.error():
            print(f"Kafka error: {msg.error()}")
            break
        else:
            record = {
                'key': msg.key(),
                'value': msg.value(),
                'topic': msg.topic(),
                'partition': msg.partition(),
                'offset': msg.offset()
            }
            messages.append(record)
            processed_messages += 1

    # 关闭消费者
    consumer.close()

    return messages