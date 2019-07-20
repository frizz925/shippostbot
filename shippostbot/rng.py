import time
from random import Random
from typing import Optional


def random_time_based(timestamp: Optional[int] = None) -> Random:
    if timestamp is None:
        timestamp = time.time()
    return Random(timestamp)
