import os
import unittest
import uuid

import boto3
from botocore.stub import Stubber

from shippostbot.storage.s3_api import S3Bucket


class TestS3API(unittest.TestCase):
    def test_api(self):
        region = 'ap-southeast-1'
        bucket_name = 'mock-bucket-' + uuid.uuid4().hex
        s3 = boto3.resource('s3', region_name=region)
        stubber = Stubber(s3.meta.client)
        s3_bucket = s3.Bucket(bucket_name)
        bucket = S3Bucket(region, s3_bucket)

        stubber.add_response('put_object', {})
        stubber.activate()

        obj = bucket.upload_blob('mock-key', b'')
        obj = bucket.get_object(obj.key)
        self.assertEqual('mock-key', obj.key)

        expected_url = 'https://s3-%s.amazonaws.com/%s/%s' % (region, bucket_name, obj.key)
        self.assertEqual(expected_url, bucket.get_public_url(obj.key))


if __name__ == '__main__':
    unittest.main()
