import logging
import os
from os import path

from dotenv import load_dotenv

import shippostbot

if __name__ == "__main__":
    if os.environ.get('DEBUG_IMAGE') == 'true':
        shippostbot.image.DEBUG_IMAGE = True
    if os.environ.get('DEBUG_LOG') == 'true':
        shippostbot.log.STDOUT_LEVEL = logging.DEBUG

    dotenv_path = path.join(path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    shippostbot.main(os.environ.get('S3_REGION'),
                     os.environ.get('S3_BUCKET_NAME'),
                     os.environ.get('FACEBOOK_ACCESS_TOKEN'),
                     os.environ.get('SELECTION_TYPE'))
