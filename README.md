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

## Keywords

To capture specific keywords or operators such as `==`, you can use a Trie:

```py
>>> from toksic import tokenize, Trie
>>> trie = Trie(); trie.insert('==')
>>> tokenize('a == b', trie)
['a', '==', 'b']

>>> trie = Trie(); trie.insert('not in')
>>> tokenize('a not in b', trie)
['a', 'not in', 'b']
```

## String literals

Only double quotes string literals are supported by default, but you can introduce other patterns as well:

```py
# Custom anything
>>> tokenize("'a$' = /b+/", literals=[("'", "'"), ("/", "/")])
["'a$'", "=", "/b+/"]

# Handle single & double quotes
>>> tokenize("'a$' = \"b+\"", literals=[("'", "'"), ('"', '"')])
["'a$'", "=", '"b+"']

# Different start & end symbols
>>> tokenize("^a+$ = \"b+\"", literals=[("^", "$"), ('"', '"')])
["^a+$", "=", '"b+"']
```

The only limitation is that your string literals must be enclosed by single character symbols, though they can be different.

## Command Line

You can also use this package to tokenize a string literal on the fly:

```sh
$ python -m toksic "a++ + -b" "++"
#                   <literal> [, <specials>]*
a
++
+
-
b
```
