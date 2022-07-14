from parser import Parser

from consts import (DIGITS, TT_DIV, TT_FLOAT, TT_INT, TT_LPAREN, TT_MINUS, TT_MUL,
                    TT_PLUS, TT_RPAREN, TT_EOF, symbol_table)
from errors import IllegalCharacterException
from models import Position, Token

from interpreter import Interpreter

###############################################################################
# TOKEN CLASS
###############################################################################




class Lexer:
    def __init__(self, filename: str, text: str):
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char: str = None
        self.advance()

    def tokenize(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                pass
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
                continue
            elif self.current_char in symbol_table:
                tokens.append(Token(symbol_table[self.current_char], pos_start=self.pos))
            else:
                pos_start = self.pos.copy()
                self.advance()
                return [], IllegalCharacterException(pos_start, self.pos, f"Illegal character found: '{self.current_char}'")

            self.advance()
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        numbers = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char and self.current_char in DIGITS:
            if self.current_char == '.':
                if dot_count > 0:
                    raise IllegalCharacterException(self.current_char)
                dot_count += 1
                numbers += '.'
                self.advance()
            else:
                numbers += self.current_char
                self.advance()
        if dot_count == 1:
            return Token(TT_FLOAT, float(numbers), pos_start=pos_start)
        return Token(TT_INT, int(numbers), pos_start=pos_start)

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(
            self.text) else None


def run(filename: str, text: str):
    lexer = Lexer(filename, text)
    tokens, error = lexer.tokenize()

    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result, ast.error
