from minio import Minio
import minio.datatypes
from django.conf import settings
import uuid


class File:
    def __init__(self, url: str, object: minio.datatypes.Object):
        self.url = url
        self.object = object


class LibraryHandler:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_API_HOST,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )

    def create_new_bucket(self):
        name = str(uuid.uuid4())
        found = self.client.bucket_exists(name)
        while found:
            name = uuid.uuid4()
            found = self.client.bucket_exists(name)
        self.client.make_bucket(name)
        return name
    
    def upload_file(self, bucket_name, file):
        self.client.fput_object(bucket_name, file, file)

    def get_file(self, bucket_name, file_name):
        return self.client.get_object(bucket_name, file_name)
    
    def get_file_url(self, bucket_name, file_name):
        return self.client.presigned_get_object(bucket_name, file_name)
    
    def get_file_list(self, bucket_name):
        objects = self.client.list_objects(bucket_name)
        files = []
        for obj in objects:
            url = self.get_file_url(bucket_name, obj.object_name)
            file = File(str(url), obj)
            files.append(file)
        return files
    