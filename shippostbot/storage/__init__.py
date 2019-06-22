from enum import Enum

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
