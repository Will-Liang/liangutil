# -*- coding: utf-8 -*-
import json

from minio import Minio

from liangutil.redisutils import RedisUtils


class MinIOUtils:

    def __init__(self, ip_port, access_key, secret_key):

        self.minioClient = Minio(ip_port, access_key,
                            secret_key, secure=False)


    # 获取MinIO中的config配置文件
    def get_jsonfile(self, bucket_name, filepath) -> dict:
        """获取MinIO中的json文件

        Args:
            bucket_name(str):桶名称
            filepath(str):文件路径

        Returns:
            dict

        """
        json_file = self.minioClient.get_object(bucket_name,filepath)
        return json.loads(json_file.data.decode("utf-8"))


    def upload_file_to_minio(self, bucket_name: str, file_path: str, current_path: str):
        """将文件上传至MinIO

        Args:
            bucket_name(str): 桶名称
            file_path(str): 上传到MinIO的文件路径
            current_path(str): 文件当前相对路径

        """

        try:
            self.minioClient.fput_object(bucket_name, file_path, current_path)
            print(current_path, "上传成功, MinIO的路径：", f"{bucket_name}/{file_path}")
        except Exception as e:
            print("出错了", e)


