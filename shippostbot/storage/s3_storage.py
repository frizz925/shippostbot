from __future__ import annotations

from boto3 import s3

from .abstracts import File, Storage
from .s3_api import S3Bucket


class S3File(File):
    storage: S3Storage

    def __init__(self,
                 storage: S3Storage,
                 s3_object: s3.Object,
                 content_type: str):
        File.__init__(self, storage, s3_object.key, content_type)
        self.s3_object = s3_object

    @property
    def public_url(self) -> str:
        return self.storage.bucket.get_public_url(self.s3_object)


class S3Storage(Storage):
    def __init__(self, bucket: S3Bucket):
        self.bucket = bucket

    @property
    def is_public(self):
        return True

    def read(self, key: str):
        res = self.bucket.get_object(key).get()
        body = res['Body']
        content = body.read()
        body.close()
        return content

    def save(self,
             key: str,
             content: bytes,
             content_type='application/octet-stream') -> S3File:
        s3_object = self.bucket.upload_blob(key, content, content_type)
        return S3File(self, s3_object, content, content_type)

    def delete(self, name: str):
        self.bucket.delete_object(name)
