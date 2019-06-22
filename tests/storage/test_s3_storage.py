import unittest
import uuid
from unittest.mock import Mock

import boto3
from botocore.response import StreamingBody
from botocore.stub import Stubber

from shippostbot.storage import S3Bucket, S3Storage


class TestS3Storage(unittest.TestCase):
    def test_storage(self):
        region = 'ap-southeast-1'
        bucket_name = 'mock-bucket-' + uuid.uuid4().hex
        s3 = boto3.resource('s3', region_name=region)
        stubber = Stubber(s3.meta.client)
        s3_bucket = s3.Bucket(bucket_name)

        bucket = S3Bucket(region, s3_bucket)
        storage = S3Storage(bucket)

        key = 'mock-key'
        mock_content = b''
        body = StreamingBody(None, len(mock_content))
        body.read = Mock(return_value=mock_content)
        body.close = Mock()

        stubber.add_response('put_object', {})
        stubber.add_response('get_object', {
            'Body': body
        })
        stubber.add_response('delete_object', {})
        stubber.activate()

        f = storage.save(key, mock_content)
        self.assertEqual(f.content, mock_content)
        f.delete()


if __name__ == '__main__':
    unittest.main()
