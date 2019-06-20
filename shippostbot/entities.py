import collections

Media = collections.namedtuple('Media', 'id title url characters')

Character = collections.namedtuple('Character', 'id first_name last_name image_url url media')

Post = collections.namedtuple('Post', 'characters media caption comment')
