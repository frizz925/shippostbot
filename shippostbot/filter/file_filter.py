import os
from typing import List, Set

from ..entities import Post

wordset = None


def load_wordlist() -> Set[str]:
    resultset = set()
    filedir = os.path.dirname(__file__)
    filename = os.path.join(filedir, 'wordlist.txt')
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if len(line) <= 0:
                break  # EOL
            word = line.strip()
            if len(word) <= 0:  # Empty, but not EOL
                continue
            elif word[0] == '#':  # Comment
                continue
            resultset.add(word)
    return resultset


def split_to_words(text: str) -> List[str]:
    return text.lower() \
        .replace(' ', '\n') \
        .splitlines()


def file_filter(post: Post) -> bool:
    global wordset
    if wordset is None:
        wordset = load_wordlist()
    for word in split_to_words(post.caption):
        if word in wordset:
            return False
    for word in split_to_words(post.comment):
        if word in wordset:
            return False
    return True
