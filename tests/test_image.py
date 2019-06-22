import unittest

from shippostbot.image import Image, ImageResizer, WandImage, combine_images


class TestImage(unittest.TestCase):
    def test_resizer(self):
        resizer = ImageResizer(400, 400)
        image = WandImage(width=200, height=300)
        size_before = image.size
        image = resizer.resize(image, 1.0)
        self.assertEqual(image.size, size_before)

    def test_resizer_exception(self):
        resizer = ImageResizer(400, 400)
        self.assertRaises(ValueError, lambda: resizer.resize(None, -1.0))

    def test_combine_images(self):
        image = combine_images(WandImage(width=300, height=300),
                               WandImage(width=200, height=200),
                               WandImage(width=100, height=400))
        self.assertIsInstance(image, Image)
        self.assertIsInstance(image.content, bytes)
        self.assertEqual(image.content_type, 'image/png')


if __name__ == '__main__':
    unittest.main()
