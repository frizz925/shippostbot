import os
from base64 import b64decode

import boto3

from shippostbot import main, set_cloudwatch, setup_from_env
from shippostbot.post import SelectionType
from shippostbot.social import Publishers
from shippostbot.storage import Storages

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
    set_cloudwatch(True)
    is_encrypted_env = 'ENCRYPTED_ENV' in os.environ
    if is_encrypted_env:
        decrypt_envs()

    setup_from_env()
    selection_type = os.environ.get('SELECTION_TYPE',
                                    SelectionType.FROM_CHARACTER_TO_MEDIA)
    result = []
    for resource in event.get('resources', []):
        if resource == 'ShippostBotFacebookScheduler':
            result.append(main(selection_type,
                               Publishers.FACEBOOK,
                               Storages.AWS_S3))
        else:
            result.append({
                'error': 'Unknown event resource: %s' % resource
            })
    return {
        'statusCode': 200,
        'data': result
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
