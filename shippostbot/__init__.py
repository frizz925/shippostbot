import sys
from hashlib import sha1

from requests import Response

from . import log
from .image import combine_images
from .post import create_post
from .social import Facebook
from .storage import S3Bucket


def main(region: str,
         bucket_name: str,
         access_token: str,
         page_id: str) -> Response:
    log.init_logger()
    logger = log.create_logger('shippostbot.main')

    post = create_post()
    if post is None:
        log.error('No anime characters found!')
        sys.exit(1)

    image = combine_images(post.first_character.image_url,
                           post.second_character.image_url)
    m = sha1()
    m.update(image)
    image_name = '%s.jpeg' % m.hexdigest()

    s3_bucket = S3Bucket(region, bucket_name)
    s3_object = s3_bucket.upload_blob(image_name, image)
    image_url = s3_bucket.get_public_url(s3_object.key)

    fb = Facebook(access_token)
    page = fb.get_page(page_id)
    res = page.publish_photo(post.caption, image_url)
    logger.info(res.json())
    res.raise_for_status()

    s3_bucket.delete_object(s3_object.key)
    return res
