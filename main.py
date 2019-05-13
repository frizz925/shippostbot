import os

import shippostbot

if __name__ == "__main__":
    shippostbot.main(os.environ['S3_REGION'],
                     os.environ['S3_BUCKET_NAME'],
                     os.environ['FACEBOOK_ACCESS_TOKEN'],
                     os.environ['FACEBOOK_PAGE_ID'])
