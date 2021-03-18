import mimetypes
import os
import pathlib
from datetime import datetime
from urllib.parse import urlparse

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from core.handlers.file_handler.file_handler import FileHandler
from core.logger.logger_handler import Logger
from core.utils.constant import Constant


class S3Handler:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, **kwargs):

        if aws_access_key_id and aws_secret_access_key:
            self.s3_resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                                              aws_secret_access_key=aws_secret_access_key,
                                              config=Config(signature_version='s3v4'))
            Logger().add_sensitive_info([aws_access_key_id, aws_secret_access_key])
        else:
            self.s3_resource = boto3.resource('s3', config=Config(signature_version='s3v4'))
        self.s3_client = self.s3_resource.meta.client
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.s3_session = None
        self.logger = Logger.get_logger()

    def get_client(self):
        return self.s3_client

    def bucket_exists(self, bucket_name):
        """Determine whether bucket_name exists and the user has permission to access it

        :param bucket_name: string
        :return: True if the referenced bucket_name exists, otherwise False
        """
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError:
            return False
        return True

    def connection_pooling(self, bucket_name):
        self.logger.info(f'Checking S3 connection to {bucket_name}')
        self.s3_client.head_bucket(Bucket=bucket_name)
        self.logger.info(f'S3 connect to {bucket_name} successfully')

    def get_s3_session(self):
        if self.s3_session:
            return self.s3_session
        return self.create_s3_session()

    def create_s3_session(self):
        if not self.aws_access_key_id:
            self.s3_session = boto3.session.Session()
        else:
            self.s3_session = boto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
        return self.s3_session

    def upload(self, filename, bucket, s3_path=None, s3_full_path=None, callback=None, extra_args=None):
        if not s3_full_path:
            if not s3_path:
                raise ValueError('We must have s3_full_path or s3_path')
            s3_full_path = os.path.join(s3_path, os.path.basename(filename))
        s3_full_path = str(pathlib.Path(s3_full_path))

        self.s3_client.upload_file(filename, bucket, s3_full_path,
                                   callback, extra_args)
        s3_url = 's3://{bucket}/{key}'.format(bucket=bucket, key=s3_full_path)
        return s3_url

    def delete_all_s3_data_from_path(self, bucket_name, path):
        if not path.endswith('/'):
            path = f'{path}/'
        bucket = self.s3_resource.Bucket(bucket_name)
        bucket.objects.filter(Prefix=path).delete()

    def copy_file(self, source_bucket_name, source_file_path, dest_bucket_name, dest_file_path):
        copy_source = {
            'Bucket': source_bucket_name,
            'Key': source_file_path
        }
        self.s3_client.copy(copy_source, dest_bucket_name, dest_file_path)

    def copy_folder(self, source_bucket_name, source_folder_path, dest_bucket_name, dest_folder_path):
        source_bucket = self.s3_resource.Bucket(source_bucket_name)

        for object_summary in source_bucket.objects.filter(Prefix=source_folder_path):
            source_file_path = object_summary.key
            dest_file_path = source_file_path.replace(source_folder_path, dest_folder_path, 1)
            self.copy_file(source_bucket_name=source_bucket_name, source_file_path=source_file_path,
                           dest_bucket_name=dest_bucket_name, dest_file_path=dest_file_path)

    def search_files_in_s3_folder_by_extension(self, path, extension):
        parse_url_result = urlparse(path)
        bucket_name = parse_url_result.netloc
        bucket = self.s3_resource.Bucket(bucket_name)
        prefix = parse_url_result.path[1:]
        file_list = []
        for file in bucket.objects.filter(Prefix=prefix):
            if file.key.endswith(extension):
                file_list.append(f'{parse_url_result.scheme}://{bucket_name}/{file.key}')
        return file_list

    @staticmethod
    def _get_bucket_name_and_file_path_from_s3_file_url(s3_url):
        parse_url_result = urlparse(s3_url)
        bucket_name = parse_url_result.netloc
        file_path = parse_url_result.path[1:]
        file_path = file_path[1:] if file_path.startswith('/') else file_path
        return bucket_name, file_path

    def download_file(self, s3_file_url, out_file_path):
        bucket_name, s3_file_path = self._get_bucket_name_and_file_path_from_s3_file_url(s3_file_url)
        self.s3_client.download_file(bucket_name, s3_file_path, out_file_path)

    def copy_file_from_external_url_to_s3(self, external_url, s3_folder_path, bucket, is_overwrite_if_exist=False):
        url_parse_obj = urlparse(external_url)
        file_name = os.path.basename(url_parse_obj.path)
        _, file_extension = os.path.splitext(url_parse_obj.path)
        s3_full_path = f'{s3_folder_path}/{file_name}'

        if not file_extension:
            file_name += Constant.EXTENSION_DEFAULT

        if not is_overwrite_if_exist and self.is_s3_path_exists_in_bucket(s3_path=s3_full_path,
                                                                          bucket_name=bucket):
            link = 's3://{bucket}/{key}'.format(bucket=bucket, key=s3_full_path)
            self.logger.info(f'File Exist! {link}')
            return link

        file_prefix = datetime.today().strftime('%Y%m%d-%H%M%S')
        tmp_file_download_path = f'/tmp/{file_prefix}_{file_name}'
        FileHandler.download_file_from_url(url=external_url, save_file_path=tmp_file_download_path)
        link = self.upload(filename=tmp_file_download_path, bucket=bucket,
                           s3_full_path=f'{s3_folder_path}/{file_name}')
        FileHandler.delete_file_path(file_path=tmp_file_download_path)
        return link

    def is_s3_path_exists_in_bucket(self, s3_path, bucket_name):
        bucket = self.s3_resource.Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=s3_path))
        if any([w.key == s3_path for w in objs]):
            return True
        return False
