import json


from minio import Minio

from liangutil.redisutils import RedisUtils


class MinIOUtils:

    def __init__(self, ip_port, access_key, secret_key):

        self.minioClient = Minio(ip_port, access_key,
                            secret_key, secure=False)


    # 获取MinIO中的config配置文件
    def get_configfile(self, bucket_name):
        config = self.minioClient.get_object(bucket_name,"config.json")
        config_json = json.loads(config.data.decode("utf-8"))

        return config_json


    # 将文件上传至MinIO，并且通知Redis
    def upload_file_to_minio_notify(self, bucket_name: str, file_path: str, current_path: str):
        '''
        将文件上传至MinIO
        :param bucket_name: 桶名称：crawl-data
        :param file_path: 上传时的文件路径
        :param current_path: 文件当前相对路径
        :return:
        '''

        try:
            # content_type="application/octet-stream"
            self.minioClient.fput_object(bucket_name, file_path, current_path)
            print(current_path, "上传成功, MinIO的路径：", bucket_name +"/"+ file_path)
            config = self.get_configfile(bucket_name)
            RedisUtils(config["mysql"]["host"], config["mysql"]["port"],
                       config["mysql"]["dbnum"], config["mysql"]["password"]).enqueue_message(file_path)
            # enqueue_message(object_name)

        except Exception as e:
            # vi_error("MinIOUtils", "upload_file_to_minio", str(e), valuelist=[object_name, file_path])
            print("出错了", e)

    # 将文件上传至MinIO
    def upload_file_to_minio(self, bucket_name: str, file_path: str, current_path: str):
        '''
        将文件上传至MinIO
        :param bucket_name: 桶名称：crawl-data
        :param file_path: 上传时的文件路径
        :param current_path: 文件当前相对路径
        :return:
        '''
        try:
            self.minioClient.fput_object(bucket_name, file_path, current_path)
            print(current_path, "上传成功, MinIO的路径：", bucket_name + "/" + file_path)
        except Exception as e:
            print("出错了", e)



