import sys

from .core import tokenize, Trie


if __name__ == '__main__':
    tstr = sys.argv[1:] and sys.argv[1]
    trie = None
    if not tstr:
        exit()
    if sys.argv[2:]:
        trie = Trie()
        for arg in sys.argv[2:]:
            trie.insert(arg)
    for token in tokenize(tstr, trie):
        print(token)
