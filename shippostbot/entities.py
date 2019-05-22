import collections

Media = collections.namedtuple('Media', 'title')

Character = collections.namedtuple('Character', 'first_name last_name image_url')

Post = collections.namedtuple('Post', 'media caption first_character second_character')
