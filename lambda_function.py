import os
from base64 import b64decode

import boto3

import shippostbot


def lambda_handler(event, context):
    try:
        crypto = CryptoHelper()
        res = shippostbot.main(crypto.env('S3_REGION'),
                               crypto.env('S3_BUCKET_NAME'),
                               crypto.env('FACEBOOK_ACCESS_TOKEN'),
                               crypto.env('FACEBOOK_PAGE_ID'))
        return {
            'statusCode': 200,
            'data': res.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }


class CryptoHelper(object):
    def __init__(self):
        self.kms = boto3.client('kms')

    def env(self, name: str) -> str:
        encrypted = os.environ.get(name)
        decrypted = self.kms.decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']
        return decrypted
