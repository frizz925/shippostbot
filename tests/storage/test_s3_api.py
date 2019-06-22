import os
import unittest
import uuid

import boto3
from moto import mock_s3

from shippostbot.storage.s3_api import S3Bucket


@mock_s3
class TestS3API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'

    def setUp(self):
        region = 'ap-southeast-1'
        bucket_name = 'mock-bucket-' + uuid.uuid4().hex
        s3 = boto3.resource('s3', region_name=region)
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': region
        })
        s3_bucket = s3.Bucket(bucket_name)

        self.s3 = s3
        self.region = region
        self.s3_bucket = s3_bucket
        self.bucket = S3Bucket(self.region, self.s3_bucket)

    def test_api(self):
        obj = self.bucket.upload_blob('mock-key', b'')
        self.assertEqual('mock-key', obj.key)

        obj = self.bucket.get_object(obj.key)
        self.assertEqual('mock-key', obj.key)

        expected_url = 'https://s3-%s.amazonaws.com/%s/%s' % (self.region, self.s3_bucket.name, obj.key)
        self.assertEqual(expected_url, self.bucket.get_public_url(obj.key))


if __name__ == '__main__':
    unittest.main()
