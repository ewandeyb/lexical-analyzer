import io

import pytest

from lexer import Lexer, Token, TokenType


@pytest.mark.parametrize(
    "input_string, expected_tokens",
    [
        (
            "IOL\nBEG x\nLOI",
            [
                Token(TokenType.IOL, None, 1, 1),
                Token(TokenType.BEG, None, 2, 1),
                Token(TokenType.IDENT, "x", 2, 5),
                Token(TokenType.LOI, None, 3, 1),
                Token(TokenType.EOF, None, 3, 4),
            ],
        ),
        (
            "INT 25",
            [
                Token(TokenType.INT, None, 1, 1),
                Token(TokenType.INT_LIT, 25, 1, 5),
                Token(TokenType.EOF, None, 1, 7),
            ],
        ),
        (
            "PRInt",
            [
                Token(TokenType.IDENT, "PRInt", 1, 1),
                Token(TokenType.EOF, None, 1, 6),
            ],
        ),
        (
            "fail?",
            [
                Token(TokenType.ERR_LEX, "fail?", 1, 1),
                Token(TokenType.EOF, None, 1, 6),
            ],
        ),
    ],
)
def test_lexer(input_string, expected_tokens):
    with io.StringIO(input_string) as stream:
        lexer = Lexer(stream)
        actual_tokens = lexer.tokenize()

    assert actual_tokens == expected_tokens
