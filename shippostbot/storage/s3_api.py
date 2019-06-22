from base64 import b64encode
from datetime import datetime, timedelta
from hashlib import md5
from typing import Optional, Union

import boto3

from ..log import create_logger

s3 = boto3.resource('s3')


class S3Bucket(object):
    def __init__(self,
                 region: str,
                 bucket: Union[str, s3.Bucket],
                 acl='private'):
        self.region = region
        self.acl = acl

        self.bucket = s3.Bucket(bucket) if isinstance(bucket, str) else bucket
        self.expiry_delta = timedelta(hours=1)
        self.logger = create_logger(S3Bucket)

    @property
    def bucket_name(self) -> str:
        return self.bucket.name

    def get_object(self, key: str) -> s3.Object:
        return self.bucket.Object(key)

    def upload_blob(self,
                    key: str,
                    blob: bytes,
                    content_type: str = 'application/octet-stream',
                    acl: Optional[str] = None) -> s3.Object:
        if acl is None:
            acl = self.acl
        expires = datetime.now() + self.expiry_delta

        self.logger.info('Putting object to S3, bucket: %s, key: %s, acl: %s, content-type: %s, expiry: %s' % (
            self.bucket.name,
            key,
            acl,
            content_type,
            expires.strftime('%Y-%m-%d %H:%M:%S')
        ))

        s3_object = self.bucket.Object(key)
        s3_object.put(ACL=acl,
                      Key=key,
                      Body=blob,
                      ContentMD5=self.hash_blob(blob),
                      ContentLength=len(blob),
                      ContentType=content_type,
                      Expires=expires)
        return s3_object

    def delete_object(self, key: str) -> dict:
        self.logger.info('Deleting object from S3, bucket: %s, key: %s' % (
            self.bucket.name,
            key
        ))
        return self.bucket.Object(key).delete()

    def hash_blob(self, blob: bytes) -> str:
        m = md5()
        m.update(blob)
        return b64encode(m.digest()).decode('utf-8')

    def get_public_url(self, key: str) -> str:
        scheme = 'https'
        host = 's3-%s.amazonaws.com' % self.region
        path = '%s/%s' % (self.bucket.name, key)
        return '%s://%s/%s' % (scheme, host, path)
