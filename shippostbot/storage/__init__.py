import os
from enum import Enum
from typing import Type, Union

from .abstracts import Storage
from .data_url_storage import DataUrlStorage
from .memory_storage import MemoryStorage
from .s3_api import S3Bucket
from .s3_storage import S3Storage
from .temp_storage import TempStorage

__all__ = [
    'S3Bucket',
    'S3Storage',
    'TempStorage',
    'MemoryStorage',
    'DataUrlStorage',
]


class Storages(Enum):
    AWS_S3 = S3Storage
    TEMP_FILE = TempStorage
    MEMORY = MemoryStorage
    DATA_URL = DataUrlStorage


def get_storage(storage: Union[str, Type[Storage]]) -> Type[Storage]:
    if isinstance(storage, Storage):
        return storage
    storage = getattr(Storages, storage, Storages.TEMP_FILE)
    if storage == Storages.AWS_S3:
        region = os.environ.get('S3_REGION')
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        bucket = S3Bucket(region, bucket_name, 'public-read')
        return Storages.AWS_S3.value(bucket)
    return storage.value()
