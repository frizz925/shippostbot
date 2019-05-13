import os
from base64 import b64decode

import boto3

import shippostbot


def lambda_handler(event, context):
    region = os.environ['S3_REGION']
    bucket_name = os.environ['S3_BUCKET_NAME']
    access_token = os.environ['FACEBOOK_ACCESS_TOKEN']
    page_id = os.environ['FACEBOOK_PAGE_ID']

    is_encrypted_env = os.environ.get('ENCRYPTED_ENV', False) == 'true'
    if is_encrypted_env:
        crypto = CryptoHelper()
        res = shippostbot.main(crypto.decrypt(region),
                               crypto.decrypt(bucket_name),
                               crypto.decrypt(access_token),
                               crypto.decrypt(page_id))
    else:
        res = shippostbot.main(region,
                               bucket_name,
                               access_token,
                               page_id)
    return {
        'statusCode': 200,
        'data': res.json()
    }


class CryptoHelper(object):
    def __init__(self):
        self.kms = boto3.client('kms')

    def decrypt(self, encrypted: str) -> str:
        decrypted = self.kms.decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']
        return decrypted
