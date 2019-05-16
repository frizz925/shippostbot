import os
from os import path

from dotenv import load_dotenv

import shippostbot

if __name__ == "__main__":
    dotenv_path = path.join(path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    shippostbot.main(os.environ['S3_REGION'],
                     os.environ['S3_BUCKET_NAME'],
                     os.environ['FACEBOOK_ACCESS_TOKEN'])
