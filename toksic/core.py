from typing import List, Optional
import string

from .trie import Trie


punctuation = """!$%&'()*+,-./:;<=>?@[\\]^_`{|}~"""


def tokenize(row: str, specials: Optional[Trie] = None) -> List[str]:

    tokens: List[str] = []
    token_vocs: List[str] = []
    quoted = False
    escaped = False
    was = None
    skip = 0

    def flush():
        nonlocal token_vocs
        nonlocal was
        # print(f'flushing while {was = }')
        was = None
        token_vocs and tokens.append(''.join(token_vocs))
        token_vocs = []

    def write(char: str):
        token_vocs.append(char)

    def print_detail():
        print(
            'Q' if quoted else '-',
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
            print(char, 'may be in specials', row[i:])
            ok, tskip = t.first(row[i:])
            print(ok, tskip)
            if ok:
                print('this is ok')
                skip += tskip
                write(row[i:i+tskip+1])
                flush()
                continue

        elif char in ['"']:
            if quoted:
                write(char)
                flush()
            else:
                flush()
                write(char)
            quoted = not quoted

        elif char == '\\':
            escaped = True
            write(char)

        elif char in string.whitespace:
            if not quoted:
                flush()
            else:
                write(char)
        
        elif char in punctuation:
            if not quoted:
                flush()
                was = ('punctuation', char)
            write(char)

        elif char == '#' and i and not quoted:
            break
            
        else:
            if was:
                # print(f'{was = }')
                flush()
            write(char)

    flush()
    print_detail()

    # if still in a literal
    if quoted:
        raise SyntaxError('Expecting a closing quote')

    return tokens
