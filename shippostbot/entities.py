from __future__ import annotations

from typing import List, NamedTuple


class Media(NamedTuple):
    id: int
    title: str
    url: str
    characters: List[Character]


class Character(NamedTuple):
    id: int
    first_name: str
    last_name: str
    image_url: str
    url: str
    media: List[Media]


class Post(NamedTuple):
    characters: List[Character]
    media: List[Media]
    caption: str
    comment: str
