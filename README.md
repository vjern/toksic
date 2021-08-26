# toksic

A character-based tokenizer for programming languages. Will tokenize:

* Identifiers;
* Number & string literals (double quotes only);
* Punctuation symbols are tokenized separately;


```py
>>> from toksic import tokenize

>>> tokenize('a + "b = c"')
['a', '+', '"b = c"']

>>> tokenize('ant+b?:c')
['ant', '+', 'b', '?', ':', 'c']

>>> tokenize('a == b')
['a', '=', '=', 'b']
```

To capture specific keywords or operators such as `==`, you can use a Trie:

```py
>>> from toksic import tokenize, Trie
>>> trie = Trie(); trie.insert('==')
>>> tokenize('a == b', trie)
['a', '==', 'b']
```

## To add

* Custom string literals (eg js-like `/regexes/`)