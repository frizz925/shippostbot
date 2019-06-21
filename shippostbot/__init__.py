import json
import sys
from hashlib import sha1

from requests import Response

from . import image, log
from .image import combine_images
from .post import SelectionType, create_post
from .social import Facebook
from .storage import S3Bucket


def main(region: str,
         bucket_name: str,
         access_token: str,
         selection_type=None) -> Response:
    log.init_logger()
    logger = log.create_logger(main)

    if selection_type is None:
        selection_type = SelectionType.FROM_MEDIA
    elif isinstance(selection_type, str):
        selection_type = getattr(SelectionType, selection_type, SelectionType.FROM_MEDIA)
    post = create_post(selection_type)
    if post is None:
        raise Exception('Can\'t create post!')
    logger.info('Post caption: ' + json.dumps(post.caption))
    logger.info('Post comment: ' + json.dumps(post.comment))

    chara_images = [c.image_url for c in post.characters]
    image = combine_images(*chara_images)
    m = sha1()
    m.update(image)
    image_name = '%s.png' % m.hexdigest()

    s3_bucket = S3Bucket(region, bucket_name)
    s3_object = s3_bucket.upload_blob(image_name, image)
    image_url = s3_bucket.get_public_url(s3_object.key)

    fb = Facebook(access_token)
    user = fb.get_user()

    res = user.publish_photo(post.caption, image_url)
    # Delete image immediately after publishing, even if it actually fails
    s3_bucket.delete_object(s3_object.key)
    res_json = res.json()
    logger.info(res_json)
    res.raise_for_status()

    post_id = res_json['post_id']
    res = fb.publish_comment(post_id, post.comment)
    logger.info(res.json())
    res.raise_for_status()

    return res
