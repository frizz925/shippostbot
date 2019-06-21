import os
from base64 import b64decode

import boto3

import shippostbot


def lambda_handler(event, context):
    shippostbot.log.CLOUDWATCH_ENABLED = True

    region = os.environ.get('S3_REGION')
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
    selection_type = os.environ.get('SELECTION_TYPE')
    logging_level = os.environ.get('LOGGING_LEVEL')

    is_encrypted_env = 'ENCRYPTED_ENV' in os.environ
    if is_encrypted_env:
        crypto = CryptoHelper()
        res = shippostbot.main(crypto.decrypt(region),
                               crypto.decrypt(bucket_name),
                               crypto.decrypt(access_token),
                               crypto.decrypt(selection_type),
                               crypto.decrypt(logging_level))
    else:
        res = shippostbot.main(region,
                               bucket_name,
                               access_token,
                               selection_type,
                               logging_level)

    return {
        'statusCode': 200,
        'data': res
    }


class CryptoHelper(object):
    def __init__(self):
        self.kms = boto3.client('kms')

    def decrypt(self, encrypted: str) -> str:
        decrypted = self.kms.decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']
        return decrypted
