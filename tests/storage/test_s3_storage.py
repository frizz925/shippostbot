import os
import unittest
import uuid

import boto3
from moto import mock_s3

from shippostbot.storage import S3Bucket, S3Storage


@mock_s3
class TestS3Storage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'

    def test_storage(self):
        region = 'ap-southeast-1'
        bucket_name = 'mock-bucket-' + uuid.uuid4().hex
        s3 = boto3.resource('s3', region_name=region)
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': region
        })
        s3_bucket = s3.Bucket(bucket_name)

        bucket = S3Bucket(region, s3_bucket)
        storage = S3Storage(bucket)

        key = 'mock-key'
        mock_content = b''

        f = storage.save(key, mock_content)
        self.assertEqual(f.content, mock_content)
        f.delete()


if __name__ == '__main__':
    unittest.main()
