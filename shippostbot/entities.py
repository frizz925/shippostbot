import collections

Anime = collections.namedtuple('Anime', 'title')

Character = collections.namedtuple(
    'Character', 'first_name last_name image_url')

Post = collections.namedtuple('Post', 'anime first_character second_character')
