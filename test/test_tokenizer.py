from pytest import mark, raises
from field_tokenizer import token_types, TokenType, tokenize, TokenizationException


@mark.parametrize('value, expected_token_types',[
    ("*", [TokenType.ALL]),
    ("5", [TokenType.NUMBER]),
    ("1-2", [TokenType.NUMBER, TokenType.RANGE_SEP, TokenType.NUMBER]),
    ("*/2", [TokenType.ALL, TokenType.STEP_SEP, TokenType.NUMBER]),
    ("1,2,3", [TokenType.NUMBER, TokenType.LIST_SEP, TokenType.NUMBER, TokenType.LIST_SEP, TokenType.NUMBER]),
])
def test_token_types(value, expected_token_types):
    actual_types = token_types(value)
    assert actual_types == expected_token_types


def test_token_unknown():
    with raises(TokenizationException):
        tokenize("&")
