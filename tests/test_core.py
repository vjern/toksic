import toksic


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
    from toksic import trie
    specials = trie.Trie()
    specials.insert('==')
    assert toksic.tokenize('a == b', specials) == ['a', '==', 'b']
    assert toksic.tokenize('a "==" b', specials) == ['a', '"=="', 'b']
