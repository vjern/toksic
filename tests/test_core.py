import toksic
from toksic import trie


toksic.core.DEBUG = True


def test_count_leading_whitespace():
    assert toksic.count_leading_whitespace('  ') == 2
    assert toksic.count_leading_whitespace('  \t') == 3


def test_level_indentation():
    rows = """
    a
        b
    """.rstrip().strip('\n').split('\n')
    assert list(toksic.level_indentation(rows)) == [
        "a",
        "    b"
    ]


def test_basic():
    assert toksic.tokenize('a + b') == ['a', '+', 'b']


def test_quotes():
    assert toksic.tokenize('a + "b  c"') == ['a', '+', '"b  c"']
    import pytest
    with pytest.raises(SyntaxError):
        toksic.tokenize('a + "b')


def test_escaped_quotes():
    assert toksic.tokenize('a + "b \\"c"') == ['a', '+', '"b \\"c"']


def test_function():
    assert toksic.tokenize('fun a(3, 2)') == ['fun', 'a', '(', '3', ',', '2', ')']
    assert toksic.tokenize('fun a(a int, b int) { return a + b }') == ['fun', 'a', '(', 'a', 'int', ',', 'b', 'int', ')', '{', 'return', 'a', '+', 'b', '}']


def test_inline_comment():
    assert toksic.tokenize('# a b') == ['#', 'a', 'b']
    assert toksic.tokenize('a # b') == ['a']
    assert toksic.tokenize('a, "#b"') == ['a', ',', '"#b"']


def test_multi_punct():
    assert toksic.tokenize('"a!"') == ['"a!"']


def test_operator():
    assert toksic.tokenize('?:') == ['?', ':']
    assert toksic.tokenize('==') == ['=', '=']
    assert toksic.tokenize('= =') == ['=', '=']


def test_specials():
    specials = trie.Trie()
    specials.insert('==')
    assert toksic.tokenize('a == b', specials) == ['a', '==', 'b']
    assert toksic.tokenize('a "==" b', specials) == ['a', '"=="', 'b']


def test_full():
    assert [c.dict() for c in toksic.tokenize('a = b')] == [
        toksic.Token('a').set('a', 0, 1).dict(),
        toksic.Token('=').set(' =', 1, 3).dict(),
        toksic.Token('b').set(' b', 3, 5).dict()
    ]
    assert [c.dict() for c in toksic.tokenize('a  = b')] == [
        toksic.Token('a').set('a', 0, 1).dict(),
        toksic.Token('=').set('  =', 1, 4).dict(),
        toksic.Token('b').set(' b', 4, 6).dict()
    ]

    assert [c.dict() for c in toksic.tokenize('@TOKEN = _ / a \tc')] == [
        toksic.Token('@').set('@', 0, 1).dict(),
        toksic.Token('TOKEN').set('TOKEN', 1, 6).dict(),
        toksic.Token('=').set(' =', 6, 8).dict(),
        toksic.Token('_').set(' _', 8, 10).dict(),
        toksic.Token('/').set(' /', 10, 12).dict(),
        toksic.Token('a').set(' a', 12, 14).dict(),
        toksic.Token('c').set(' \tc', 14, 17).dict(),
    ]


def test_custom_literals():

    assert toksic.tokenize('"a = b"') == ['"a = b"']
    assert toksic.tokenize("'a = b'", literals=[("'", "'")]) == ["'a = b'"]
    assert toksic.tokenize("/a = b/", literals=[("/", "/")]) == ["/a = b/"]
    assert toksic.tokenize("{a = b}", literals=[("{", "}")]) == ["{a = b}"]

    assert toksic.tokenize(""" 'b =' + "'a' = b" """, literals=[("'", "'"), ('"', '"')]) == ["'b ='", "+", "\"'a' = b\""]
    assert toksic.tokenize("'b =' + {'a' = b}", literals=[("'", "'"), ("{", "}")]) == ["'b ='", "+", "{'a' = b}"]
