import json
import os
import sys
from os import path

import shippostbot

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        dotenv_path = path.join(path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)
    except ImportError:
        pass

    if os.environ.get('DEBUG_IMAGE') == 'true':
        shippostbot.image.DEBUG_IMAGE = True

    res = shippostbot.main(os.environ.get('S3_REGION'),
                           os.environ.get('S3_BUCKET_NAME'),
                           os.environ.get('FACEBOOK_ACCESS_TOKEN'),
                           os.environ.get('SELECTION_TYPE'),
                           os.environ.get('LOGGING_LEVEL'))
    sys.stdout.write(json.dumps(res))
    sys.stdout.flush()
