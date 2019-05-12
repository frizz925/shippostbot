from multiprocessing.pool import ThreadPool

import requests
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.image import Image


def combine_images(*images_url: list) -> bytes:
    pool = ThreadPool(2)
    images = pool.map(fetch_image, images_url)
    images = [Image(blob=img) for img in images]

    max_image = max(images, key=lambda x: x.height)
    max_height = max_image.height

    sum_width = sum([x.width for x in images])
    canvas = Image(width=sum_width, height=max_height)

    left = 0
    draw = Drawing()
    draw.fill_color = Color('white')
    draw.rectangle(left=0, top=0, right=canvas.width, bottom=canvas.height)
    draw(canvas)

    for img in images:
        draw.composite(operator='replace',
                       top=0, left=left,
                       width=img.width, height=img.height,
                       image=img)
        draw(canvas)
        left += img.width

    display(canvas)
    return canvas.make_blob(format='jpeg')


def fetch_image(image_url: str) -> bytes:
    res = requests.get(image_url, stream=True)
    return res.content
