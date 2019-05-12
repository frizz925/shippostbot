from hashlib import sha1

from shippostbot import log
from shippostbot.image import combine_images
from shippostbot.post import create_post
from shippostbot.storage import S3Bucket

S3_BUCKET_NAME = 'shippostbot'

if __name__ == "__main__":
    log.init_logger()
    post = create_post()

    image = combine_images(post.first_character.image_url,
                           post.second_character.image_url)
    m = sha1()
    m.update(image)
    image_name = m.hexdigest()

    s3_bucket = S3Bucket(S3_BUCKET_NAME)
    res = s3_bucket.upload_blob(image_name, image)
    # res = s3_bucket.delete_object(res.key)
    log.info(res)
