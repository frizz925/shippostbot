import json
import logging
import os
from hashlib import sha1

from . import log
from .image import combine_images
from .post import SelectionType, create_post
from .social import Facebook
from .storage import S3Bucket


def main(region=None,
         bucket_name=None,
         access_token=None,
         selection_type=None,
         logging_level=None) -> dict:
    if isinstance(logging_level, str):
        log.LOGGING_LEVEL = getattr(logging, logging_level, log.LOGGING_LEVEL)
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
    image_url = None

    if region is not None and bucket_name is not None:
        s3_bucket = S3Bucket(region, bucket_name)
        s3_object = s3_bucket.upload_blob(image_name, image)
        image_url = s3_bucket.get_public_url(s3_object.key)

        if access_token is not None:
            fb = Facebook(access_token)
            user = fb.get_user()

            res = user.publish_photo(post.caption, image_url)
            # Delete image immediately after publishing, even if it actually fails
            s3_bucket.delete_object(s3_object.key)
            res_json = res.json()
            logger.info(res_json)
            res.raise_for_status()

            user_id = res_json['id']
            post_id = res_json['post_id']

            res = fb.publish_comment(post_id, post.comment)
            res_json = res.json()
            logger.info(res_json)
            res.raise_for_status()

            comment_id = res_json['id']
            return {
                'user_id': user_id,
                'post_id': post_id,
                'comment_id': comment_id,
            }
    else:
        image_path = os.path.join(os.getcwd(), 'images', image_name)
        with open(image_path, 'wb') as f:
            f.write(image)
        image_url = 'file://%s' % image_path

    return {
        'caption': post.caption,
        'comment': post.comment,
        'image_url': image_url,
    }
