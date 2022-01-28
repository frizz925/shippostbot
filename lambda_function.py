import os
from base64 import b64decode
from multiprocessing.pool import ThreadPool
from typing import List, Union

import boto3

from shippostbot import main, set_cloudwatch, setup_from_env
from shippostbot.entities import Character, Media
from shippostbot.filter import Filters
from shippostbot.post import SelectionType
from shippostbot.social import Publishers
from shippostbot.storage import Storages

LAMBDA_ENVS = [
    # AWS S3
    'S3_REGION',
    'S3_BUCKET_NAME',

    # AWS CloudWatch Events,
    'EVENT_FACEBOOK_ARN',

    # Facebook
    'FACEBOOK_ACCESS_TOKEN',
    'FACEBOOK_PUBLISH_STYLE',

    # Misc
    'SELECTION_TYPE',
    'SOCIAL_PUBLISHER',
    'STORAGE_TYPE',
    'LOGGING_LEVEL',
    'ENCRYPTED_ENV'
]


def lambda_handler(event: dict, context: any) -> dict:
    set_cloudwatch(True)
    is_encrypted_env = 'ENCRYPTED_ENV' in os.environ
    if is_encrypted_env:
        decrypt_envs()

    setup_from_env()
    selection_type = os.environ.get('SELECTION_TYPE',
                                    SelectionType.FROM_CHARACTER_TO_MEDIA)
    resources = event.get('resources', [])
    with ThreadPool() as pool:
        results = pool.map(lambda x: exec_resource(selection_type, x), resources)
    return {
        'results': results
    }


def exec_resource(selection_type: Union[str, SelectionType],
                  resource: str) -> dict:
    if resource == os.environ.get('EVENT_FACEBOOK_ARN'):
        return main(selection_type,
                    publisher=Publishers.FACEBOOK,
                    storage=Storages.AWS_S3,
                    comment_fn=facebook_comment,
                    filter_fn=Filters.FILE)
    else:
        raise Exception('Unknown event resource: %s' % resource)


def facebook_comment(characters: List[Character],
                     media: List[Media]) -> str:
    comment = 'Source(s):\r\n'
    comment += '\r\n'.join('%s: %s' % (m.title, m.url) for m in media)
    return comment


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
