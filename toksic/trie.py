from dataclasses import dataclass, field
from typing import List, Any, Dict, Tuple, Optional, Set


class _Any:
    def __str__(self): return 'ANY'
    def __repr__(self): return str(self)


class _EqAll:
    def __str__(self): return 'ROOT'
    def __repr__(self): return str(self)
    def __eq__(self, o):
        return True


# from .tree import Node
_any = _Any()
_any_n = object()  # 1 or n


@dataclass
class Trie:

    children: Dict[Any, 'Trie'] = field(default_factory=dict)
    leaves: Set[Any] = field(default_factory=set)
    # name: Optional[str] = _EqAll()

    def insert(self, items: List) -> int:
        if not items:
            return 1
        first = items[0]
        if first is _any_n:
            child = self.children[_any] = self.children.get(_any, self)
            # child.name = 'ANY'
            first = _any
        child = self.children[first] = self.children.get(first, Trie())
        child.name = str(first)
        res = child.insert(items[1:])
        if res:
            self.leaves.add(first)
        return 0

    def has(self, item: Any) -> bool:
        return item in self.children
    
    def get(self, item: Any) -> Optional['Trie']:
        return self.children.get(item)

    def __getitem__(self, key):
        return self.children[key]

    # hot mess to pass all tests (especially any)
    def find(self, items: List, take_first: bool = False) -> Tuple[bool, int]:
        skip = 1
        ans = False
        if not items:
            return (False, 0)
        first = items[0]
        if (take_first or not items[1:]) and (first in self.leaves or _any in self.leaves):
            print(f'found {first} in leaves of {self}')
            return (True, 1)
        t = self.children.get(first)
        if t:
            ans, cskip = t.find(items[1:], take_first=take_first)
            skip += cskip
        elif _any in self.children:
            ans = take_first
            cans, cskip = self.children[_any].find(items[1:], take_first=take_first)
            if cskip:
                ans = cans
            if not ans:
                print('Could not find', items[1:], 'in any from', self, first)
            skip += cskip
        return (ans, skip)

    def first(self, items):
        return self.find(items, take_first=True)


def from_string(pat: str) -> list:
    tokens = pat.split()
    for i, token in enumerate(tokens):
        if token == '_+':
            token = _any_n
        elif token == '_':
            token = _any
        tokens[i] = token
    return tokens


class TestTrie:

    def test_find(self):

        t = Trie()
        t.insert('a')
        assert t == Trie(
            { 'a': Trie() },
            { 'a' }
        )
        assert t.find('a') == (True, 1)
        assert t.find('b') == (False, 1)

        t = Trie()
        t.insert('ab')
        assert t == Trie(
            {
                'a': Trie(
                    { 'b': Trie() },
                    { 'b' }
                )
            },
            set()
        )
        assert t.find('a') == (False, 1)
        assert t.find('ab') == (True, 2)
        assert t.find('db') == (False, 1)
        assert t.find('ac') == (False, 2)

        t = Trie()
        t.insert('ab')
        t.insert('ac')
        assert t == Trie(
            {
                'a': Trie(
                    { 'b': Trie(), 'c': Trie() },
                    { 'b', 'c' }
                )
            }
        )
        assert t.find('a') == (False, 1)
        assert t.find('ab') == (True, 2)
        assert t.find('ac') == (True, 2)
        assert t.find('db') == (False, 1)
        assert t.find('dc') == (False, 1)


    def test_first(self):

        t = Trie()
        t.insert('==')
        assert t == Trie(
            {
                '=': Trie(
                    { '=': Trie() },
                    { '=' }
                )
            }
        )
        assert t.find('==') == (True, 2)
        assert t.find('== a') == (False, 3)
        
        assert t.find('==', take_first=True) == (True, 2)
        assert t.find('== a', take_first=True) == (True, 2)

        assert t.first('==') == (True, 2)
        assert t.first('== a') == (True, 2)


    def test_list(self):

        t = Trie()
        t.insert([0, 1])
        assert t == Trie(
            {
                0: Trie(
                    { 1: Trie() },
                    { 1 }
                )
            }
        )
        assert t.find([0, 1]) == (True, 2)
        assert t.find([1, 1]) == (False, 1)
        assert t.find([0, 2]) == (False, 2)
        assert t.find([0, 2, 55]) != (False, 3)
        
        assert t.first([0, 2, 55]) != (True, 2)


    def test_any(self):

        t = Trie()
        t.insert([_any, 1])
        assert t == Trie(
            {
                _any: Trie(
                    { 1: Trie() },
                    { 1 }
                )
            }
        )
        assert t.find([0, 1]) == (True, 2)
        assert t.find([1, 1]) == (True, 2)
        assert t.find([1, 2]) == (False, 2)

        assert t.first([1, 1, 3]) == (True, 2)
        assert t.first([0, 1, 3]) == (True, 2)


    def test_any_multiple(self):

        t = Trie()
        t.insert([_any, 1, _any, 1])
        assert t == Trie(
            {
                _any: Trie(
                    { 1: Trie(
                        { _any: Trie(
                            { 1: Trie() },
                            { 1 }
                        ) },
                    ) }
                )
            }
        )
        assert t.find([0, 1, 2, 1]) == (True, 4)
        assert t.find([1, 1, 2, 1]) == (True, 4)
        assert t.find([1, 2, 2, 1]) == (False, 2)


    def test_any_ending(self):

        t = Trie()
        t.insert([_any, 1, _any])
        assert t == Trie(
            {
                _any: Trie(
                    { 1: Trie(
                        { _any: Trie() },
                        { _any }
                    ) }
                )
            }
        )
        assert t.find([0, 1, 2]) == (True, 3)
        assert t.find([1, 1, 2]) == (True, 3)
        assert t.find([1, 2, 2]) == (False, 2)
        
        assert t.first([0, 1, 2, 3]) == (True, 3)
        assert t.first([1, 1, 2, 3]) == (True, 3)
        assert t.first([1, 2, 2, 3]) == (False, 2)


    def test_consecutive_any(self):

        t = Trie()
        t.insert([_any, _any, 1, 3])
        assert t == Trie(
            { _any: Trie (
                { _any: Trie(
                    { 1: Trie(
                        { 3: Trie() },
                        { 3 }
                    ) }
                ) }
            ) }
        )
        assert t.find([1, 2, 1, 3]) == (True, 4)
        assert t.find([33, 44, 1, 3]) == (True, 4)
        assert t.find([0, 0, 0, 3]) == (False, 3)
        
        assert t.first([0, 0, 1, 3, 5, 5]) == (True, 4)

        t.insert([_any, _any])
        assert t == Trie(
            { _any: Trie (
                { _any: Trie(
                    { 1: Trie(
                        { 3: Trie() },
                        { 3 }
                    ) }
                ) },
                { _any }
            ) }
        )
        assert t.find([1, 2, 1, 3]) == (True, 4)
        assert t.first([1, 2, 1, 3]) == (True, 2)

        t.insert([_any, _any, 1, 3, _any, _any])
        assert t == Trie(
            { _any: Trie (
                { _any: Trie(
                    { 1: Trie(
                        { 3: Trie(
                            { _any: Trie(
                                { _any: Trie() },
                                { _any }
                            ) }
                        ) },
                        { 3 }
                    ) }
                ) },
                { _any }
            ) }
        )
        assert t.find([0, 0, 1, 3, 0, 2]) == (True, 6)
        assert t.find([0, 0, 1, 3, 4, 7]) == (True, 6)


    def test_any_trailing(self):
        t = Trie()
        t.insert([_any, _any])
        assert t.find([3, 4]) == (True, 2)
        assert t.find([3, 4, 5]) == (False, 3)
        assert t.first([2, 5, 7]) == (True, 2)
        assert t.find([2]) == (False, 1)


    def test_any_n(self):

        t = Trie()
        t.insert([_any_n, 333])
        assert t == Trie(
            { _any: t, 333: Trie() },
            { 333 }
        )
        assert t.find([3, 4, 333]) == (True, 3)
        assert t.find([3, 333]) == (True, 2)
        assert t.find([333]) == (True, 1)
        
        assert t.first([3, 4, 333, 222]) == (True, 3)
        assert t.first([3, 333, 3]) == (True, 2)


    def test_any_n_only(self):

        t = Trie()
        t.insert([_any_n])
        assert t == Trie(
            { _any: t },
            { _any }
        )
        assert t.find([3, 4, 333]) == (True, 3)
        assert t.find([3, 333]) == (True, 2)
        assert t.find([333]) == (True, 1)
        
        assert t.first([3, 4, 333, 222]) == (True, 1)
        assert t.first([3, 333, 3]) == (True, 1)


    def test_multi_any_n(self):

        t = Trie()
        t.insert([_any_n, 3, _any_n, 33])
        assert t == Trie({
            _any: t,
            3: Trie(
                {
                    _any: t.children[3],
                    33: Trie()
                },
                { 33 }
            )
        })

        assert t.find([0, 3, 4, 33]) == (True, 4)
        assert t.find([0, 0, 3, 4, 33]) == (True, 5)
        assert t.find([0, 0, 3, 4, 77, 33]) == (True, 6)
        
        assert t.first([0, 3, 4, 33, 55]) == (True, 4)
        assert t.first([0, 0, 3, 4, 33, 77]) == (True, 5)
        assert t.first([0, 0, 3, 4, 77, 33, 66]) == (True, 6)


    def test_trailing_any_n(self):

        t = Trie()
        t.insert([99, _any_n])
        assert t == Trie(
            { 99: Trie(
                { _any: t.children[99] },
                { _any }
            ) }
        )

        # greedy
        assert t.find([99, 3, 4, 333]) == (True, 4)
        assert t.find([99, 3, 333]) == (True, 3)
        assert t.find([99, 333]) == (True, 2)
        
        # non greedy
        assert t.first([99, 3, 4, 333, 222]) == (True, 2)
        assert t.first([99, 3, 333, 3]) == (True, 2)


    def test_consecutive_any_n(self):

        t = Trie()
        t.insert([_any_n, _any_n, 333])
        assert t == Trie(
            { _any: t, 333: Trie() },
            { 333 }
        )
        assert t.find([3, 4, 333]) == (True, 3)
        assert t.find([3, 333]) == (True, 2)
        assert t.find([333]) == (True, 1)
        
        assert t.first([3, 4, 333, 222]) == (True, 3)
        assert t.first([3, 333, 3]) == (True, 2)


    def test_any_n_ambiguous(self):

        t = Trie()
        t.insert([_any_n, 33])
        assert t.find([0, 33, 33]) == (False, 3)  # only the first 


    def test_from_string(self):
        assert from_string('_ + _') == [_any, '+', _any]
        assert from_string('_ ? _+ : _+') == [_any, '?', _any_n, ':', _any_n] 


# still need to be able to tell the spans positions captured by any_n