import logging
from base64 import b64encode
from datetime import datetime, timedelta
from hashlib import md5

import boto3

s3 = boto3.resource('s3')


class S3Bucket(object):
    def __init__(self, region: str, bucket_name: str):
        self.region = region
        self.bucket_name = bucket_name
        self.bucket = s3.Bucket(bucket_name)
        self.expiry_delta = timedelta(hours=1)

    def upload_blob(self, name: str, blob: bytes,
                    content_type='image/jpeg') -> s3.Object:
        expires = datetime.now() + self.expiry_delta
        logging.info('Uploading object to S3, bucket: %s, key: %s, expiry: %s' % (
            self.bucket_name,
            name,
            expires.strftime('%Y-%m-%d %H:%M:%S')
        ))
        return self.bucket.put_object(ACL='public-read',
                                      Key=name,
                                      Body=blob,
                                      ContentMD5=self.hash_blob(blob),
                                      ContentLength=len(blob),
                                      ContentType=content_type,
                                      Expires=expires)

    def delete_object(self, name: str) -> dict:
        logging.info('Deleting object from S3, bucket: %s, key: %s' % (
            self.bucket_name,
            name
        ))
        return self.bucket.delete_objects(Delete={
            'Objects': [{
                'Key': name
            }]
        })

    def hash_blob(self, blob: bytes) -> str:
        m = md5()
        m.update(blob)
        return b64encode(m.digest()).decode('utf-8')

    def get_public_url(self, key: str) -> str:
        scheme = 'https'
        host = 's3-%s.amazonaws.com' % self.region
        path = '%s/%s' % (self.bucket_name, key)
        return '%s://%s/%s' % (scheme, host, path)
