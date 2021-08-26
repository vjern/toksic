import toksic as parse
from toksic import trie


def test_count_leading_whitespace():
    assert parse.count_leading_whitespace('  ') == 2
    assert parse.count_leading_whitespace('  \t') == 3


def test_level_indentation():
    rows = """
    a
        b
    """.rstrip().strip('\n').split('\n')
    assert list(parse.level_indentation(rows)) == [
        "a",
        "    b"
    ]


def test_basic():
    assert parse.tokenize('a + b') == ['a', '+', 'b']


def test_quotes():
    assert parse.tokenize('a + "b  c"') == ['a', '+', '"b  c"']
    import pytest
    with pytest.raises(SyntaxError):
        parse.tokenize('a + "b')


def test_escaped_quotes():
    assert parse.tokenize('a + "b \\"c"') == ['a', '+', '"b \\"c"']


def test_function():
    assert parse.tokenize('fun a(3, 2)') == ['fun', 'a', '(', '3', ',', '2', ')']
    assert parse.tokenize('fun a(a int, b int) { return a + b }') == ['fun', 'a', '(', 'a', 'int', ',', 'b', 'int', ')', '{', 'return', 'a', '+', 'b', '}']


def test_inline_comment():
    assert parse.tokenize('# a b') == ['#', 'a', 'b']
    assert parse.tokenize('a # b') == ['a']
    assert parse.tokenize('a, "#b"') == ['a', ',', '"#b"']


def test_multi_punct():
    assert parse.tokenize('"a!"') == ['"a!"']


def test_operator():
    assert parse.tokenize('?:') == ['?', ':']
    assert parse.tokenize('==') == ['=', '=']
    assert parse.tokenize('= =') == ['=', '=']


def test_specials():
    specials = trie.Trie()
    specials.insert('==')
    assert parse.tokenize('a == b', specials) == ['a', '==', 'b']
    assert parse.tokenize('a "==" b', specials) == ['a', '"=="', 'b']


def test_full():
    assert [c.dict() for c in parse.tokenize('a = b')] == [
        parse.Token('a').set('a', 0, 1).dict(),
        parse.Token('=').set(' =', 1, 3).dict(),
        parse.Token('b').set(' b', 3, 5).dict()
    ]
    assert [c.dict() for c in parse.tokenize('a  = b')] == [
        parse.Token('a').set('a', 0, 1).dict(),
        parse.Token('=').set('  =', 1, 4).dict(),
        parse.Token('b').set(' b', 4, 6).dict()
    ]

    assert [c.dict() for c in parse.tokenize('@TOKEN = _ / a \tc')] == [
        parse.Token('@').set('@', 0, 1).dict(),
        parse.Token('TOKEN').set('TOKEN', 1, 6).dict(),
        parse.Token('=').set(' =', 6, 8).dict(),
        parse.Token('_').set(' _', 8, 10).dict(),
        parse.Token('/').set(' /', 10, 12).dict(),
        parse.Token('a').set(' a', 12, 14).dict(),
        parse.Token('c').set(' \tc', 14, 17).dict(),
    ]
