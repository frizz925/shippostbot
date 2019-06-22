import os
from multiprocessing.pool import ThreadPool
from statistics import mean
from typing import List, NamedTuple, Union

import requests
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.image import Image as WandImage

DEBUG_IMAGE = False


class Image(NamedTuple):
    content: bytes
    content_type: str


class ImageResizer(object):
    def __init__(self, max_width: int, max_height: int):
        self.max_width = max_width
        self.max_height = max_height

    def resize(self, img: WandImage, mult: float) -> WandImage:
        # No need to waste our resources for resizing by the same exact multiplier (1:1)
        if mult == 1.0:
            return img
        # Or even invalid multiplier (raise exception instead)
        elif mult <= 0:
            raise ValueError("Image resize multiplier must not be less than 0!")

        # Resize the image using the multiplier
        new_width = round(img.width * mult)
        new_height = round(img.height * mult)
        img.adaptive_resize(new_width, new_height)

        # Then crop the image so it's centered
        crop_left = round((self.max_width - img.width) / 2)
        if crop_left < 0:
            crop_left = 0
        crop_right = crop_left + self.max_width
        if crop_right > img.width:
            crop_right = img.width
        img.crop(crop_left, 0, crop_right, self.max_height)

        return img


def combine_images(*images: List[Union[str, bytes, WandImage]]) -> Image:
    with ThreadPool() as pool:
        images = pool.map(normalize_image, images)

    max_width = round(mean(img.width for img in images))
    max_height = round(mean(img.height for img in images))
    sum_width = max_width * len(images)

    canvas = WandImage(width=sum_width, height=max_height)
    resizer = ImageResizer(max_width, max_height)

    left = 0
    draw = Drawing()
    draw.fill_color = Color('white')
    draw.rectangle(left=0, top=0, right=canvas.width, bottom=canvas.height)
    draw(canvas)

    for img in images:
        if img.height < max_height:
            img = resizer.resize(img, max_height / img.height)

        if img.width < max_width:
            img = resizer.resize(img, max_width / img.width)
        elif img.width > max_width:
            # Do a bit of cropping so it's centered
            crop_left = round((img.width - max_width) / 2)
            crop_right = crop_left + max_width
            img.crop(crop_left, 0, crop_right, img.height)

        draw.composite(operator='over',
                       top=0, left=left,
                       width=img.width, height=img.height,
                       image=img)
        draw(canvas)
        left += img.width

    if DEBUG_IMAGE:  # pragma: no cover
        server_name = os.environ.get('DISPLAY', ':0')
        display(canvas, server_name=server_name)

    return Image(content=canvas.make_blob(format='png'),
                 content_type='image/png')


def normalize_image(image: Union[str, bytes, WandImage]) -> WandImage:
    if isinstance(image, str):
        image = fetch_image(image)
    if isinstance(image, bytes):
        return WandImage(blob=image)
    return image


def fetch_image(image_url: str) -> bytes:
    res = requests.get(image_url, stream=True)
    return res.content
