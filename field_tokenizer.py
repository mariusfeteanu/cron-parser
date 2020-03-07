from typing import List, Tuple
from enum import Enum, auto

from model import *


class TokenizationException(Exception):
    pass

class TokenType(Enum):
    NUMBER = auto()
    ALL = auto()
    STEP = auto()
    RANGE = auto()
    LIST = auto()

    def __repr__(self):  # pragma: no cover
        return self.name


SIMPLE_TOKENS = {
    '*': TokenType.ALL,
    '/': TokenType.STEP,
    '-': TokenType.RANGE,
    ',': TokenType.LIST
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
    current_token_type = None
    
    for c in remaining[ii:]:
        simple_token = SIMPLE_TOKENS.get(c)
        if simple_token is not None and current_token_type is None:
            ii += 1
            current_token_type = simple_token
            break
        if c in '0123456789' and (current_token_type is None or current_token_type == TokenType.NUMBER):
            ii += 1
            if current_token_type is None:
                current_token_type = TokenType.NUMBER
        else:
            break
    
    if current_token_type is not None:
        return Token(current_token_type, remaining[:ii]), remaining[ii:]
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
