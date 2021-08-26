import string
from builtins import print as builtin_print
from typing import List, Optional, Tuple

from .trie import Trie


punctuation = set(string.punctuation) - {"_", '"', "#", "-"}
DEBUG = False
DEBUG = True


def count_leading_whitespace(row: str) -> int:
    total = 0
    for c in row:
        t = {' ': 1, '\t': 4}.get(c, -1)
        if t == -1:
            break
        total += 1
    return total


def level_indentation(rows: List[str]) -> List[str]:
    rows = list(rows)
    # check lowest common level of indentation
    mlen = max(0, min(map(count_leading_whitespace, rows)))
    # strip it
    for row in rows:
        # assert not r[:l].strip(), (l, repr(r[:l]))
        yield row[mlen:]


def print(*a, **kw):
    if DEBUG:
        builtin_print(*a, **kw)


class Token(str):
    bounds: Tuple[int, int]
    string: str

    def set(self, string: str, *bounds: int):
        self.bounds = bounds
        self.string = string
        return self

    def dict(self):
        return {
            'text': str(self),
            'bounds': self.bounds,
            'string': self.string
        }


def tokenize(
    row: str,
    specials: Optional[Trie] = None,
    literals: List[Tuple[str, str]] = [('"', '"')]
) -> List[str]:

    literals_dict = {a: b for a, b in literals}

    tokens: List[str] = []
    token_vocs: List[str] = []
    closing_quote = None
    quoted = False
    escaped = False
    was = None
    past = 0
    skip = 0

    def flush(i):
        nonlocal token_vocs
        nonlocal was
        nonlocal past
        was = None
        if token_vocs:
            token = ''.join(token_vocs)
            bounds, past = (past, i), i
            a, b = bounds
            token = Token(token).set(row[a:b], *bounds)
            tokens.append(token)
            token_vocs = []

    def write(char: str):
        token_vocs.append(char)

    def print_detail():
        print(
            'Q' + closing_quote if quoted else '--',
            row[:i] + '\033[92;1m' + char + '\033[m' + row[i + 1:],
            tokens,
            ''.join(token_vocs),
        )

    for i, char in enumerate(row):

        print_detail()

        if skip:
            skip -= 1
            continue

        if escaped:
            escaped = False
            write(char)
            continue

        t = not quoted and specials and specials.get(char)
        if t:
            print(char, 'may be in specials', repr(row[i:]))
            ok, tskip = specials.first(row[i:])
            print(ok, tskip)
            if ok:
                print('this is ok')
                skip += tskip
                flush(i)
                write(row[i:i + tskip])
                flush(i + tskip)
                continue

        if quoted and char == closing_quote:
            write(char)
            flush(i)
            quoted = False
            closing_quote = None

        elif not quoted and char in literals_dict:
            flush(i)
            write(char)
            closing_quote = literals_dict[char]
            print('found string literal', char, closing_quote)
            quoted = True

        elif char == '\\':
            escaped = True
            write(char)

        elif char in string.whitespace:
            if not quoted:
                flush(i)
            else:
                write(char)

        elif char in punctuation:
            if not quoted:
                flush(i)
                was = ('punctuation', char)
            write(char)

        elif char == '#' and i and not quoted:
            break

        else:
            if was:
                # print(f'{was = }')
                flush(i)
            write(char)

    flush(i + 1)
    print_detail()

    # if still in a literal
    if quoted:
        raise SyntaxError(f'Expecting a closing quote {closing_quote}')

    return tokens


def retrace_tokens(tokens: List[Token]) -> str:
    return ''.join(t.string for t in tokens)
