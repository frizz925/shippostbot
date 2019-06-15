import collections

Media = collections.namedtuple('Media', 'title url')

Character = collections.namedtuple('Character', 'first_name last_name image_url url')

Post = collections.namedtuple('Post', 'characters media caption comment')
