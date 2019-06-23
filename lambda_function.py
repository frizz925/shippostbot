import os
from base64 import b64decode

import boto3

import shippostbot

LAMBDA_ENVS = [
    # AWS S3
    'S3_REGION',
    'S3_BUCKET_NAME',

    # Facebook
    'FACEBOOK_ACCESS_TOKEN',

    # Misc
    'SELECTION_TYPE',
    'SOCIAL_PUBLISHER',
    'STORAGE_TYPE',
    'LOGGING_LEVEL',
    'ENCRYPTED_ENV'
]


def lambda_handler(event, context):
    shippostbot.set_cloudwatch(True)

    is_encrypted_env = 'ENCRYPTED_ENV' in os.environ
    if is_encrypted_env:
        decrypt_envs()

    shippostbot.setup_from_env()
    res = shippostbot.main(event['selection_type'],
                           event['publisher'],
                           event['storage'])
    return {
        'statusCode': 200,
        'data': res
    }


def decrypt_envs():
    crypto = CryptoHelper()
    for name in LAMBDA_ENVS:
        value = os.environ.get(name)
        if value is None:
            continue
        os.environ[name] = crypto.decrypt(value)


class CryptoHelper(object):
    def __init__(self):
        self.kms = boto3.client('kms')

    def decrypt(self, encrypted: str) -> str:
        decrypted = self.kms.decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']
        return decrypted
