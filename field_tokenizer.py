from typing import List, Tuple
from enum import Enum, auto

from model import *


class TokenizationException(Exception):
    pass

class TokenType(Enum):
    NUMBER = auto()
    ALL = auto()
    STEP_SEP = auto()
    RANGE_SEP = auto()
    LIST_SEP = auto()

    def __repr__(self):  # pragma: no cover
        return self.name


SIMPLE_TOKENS = {
    '*': TokenType.ALL,
    '/': TokenType.STEP_SEP,
    '-': TokenType.RANGE_SEP,
    ',': TokenType.LIST_SEP
    }

@dataclass
class Token:
    token_type: TokenType
    value: str

    def __repr__(self):  # pragma: no cover
        if self.token_type in SIMPLE_TOKENS.values():
            return str(self.token_type.name)
        return f'{self.token_type.name}: {self.value}'

def next_token(remaining: str) -> Tuple[Token, str]:
    
    ii = 0
    token_type = None
    
    for c in remaining[ii:]:
        if c in SIMPLE_TOKENS and token_type is None:
            ii += 1
            token_type = SIMPLE_TOKENS[c]
            break
        if c in '0123456789' and (token_type is None or token_type == TokenType.NUMBER):
            ii += 1
            if token_type is None:
                token_type = TokenType.NUMBER
        else:
            break
    
    if token_type is not None:
        return Token(token_type, remaining[:ii]), remaining[ii:]
    else:
        raise TokenizationException(f'Unrecognized token: "{c}" from "{remaining}"')


def tokenize(field: str) -> List[Token]:
    tokens = []
    while(field):
        token, field = next_token(field)
        tokens.append(token)
    return tokens


def token_types(field: str) -> List[TokenType]:
    return [token.token_type for token in tokenize(field)]
