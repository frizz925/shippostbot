import unittest

import boto3
from botocore import stub

from shippostbot.storage.s3_api import S3Bucket


class TestS3API(unittest.TestCase):
    def setUp(self):
        s3 = boto3.resource('s3')
        stubber = stub.Stubber(s3.meta.client)

        self.s3 = s3
        self.region = 'ap-southeast-1'
        self.s3_bucket = s3.Bucket('mock-bucket')
        self.bucket = S3Bucket(self.region, self.s3_bucket)
        self.stubber = stubber

    def test_get_object(self):
        self.stubber.activate()
        obj = self.bucket.get_object('mock-object')
        self.assertEqual('mock-object', obj.key)

    def test_upload_blob(self):
        expected_params = {
            'ACL': 'private',
            'Body': b'',
            'Bucket': self.s3_bucket.name,
            'ContentLength': 0,
            'ContentMD5': stub.ANY,
            'ContentType': 'application/octet-stream',
            'Expires': stub.ANY,
            'Key': 'mock-blob',
        }
        self.stubber.add_response('put_object', {}, expected_params)
        self.stubber.activate()

        obj = self.bucket.upload_blob(expected_params['Key'],
                                      expected_params['Body'],
                                      expected_params['ContentType'])
        self.assertEqual(expected_params['Key'], obj.key)

    def test_get_public_url(self):
        key = 'mock-key'
        expected_url = 'https://s3-%s.amazonaws.com/%s/%s' % (self.region, self.s3_bucket.name, key)
        self.assertEqual(expected_url, self.bucket.get_public_url(key))


if __name__ == '__main__':
    unittest.main()
