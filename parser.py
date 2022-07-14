from consts import (TT_DIV, TT_FLOAT, TT_INT, TT_LPAREN, TT_MINUS, TT_MUL,
                    TT_PLUS, TT_RPAREN, TT_EOF)
from errors import InvalidSyntaxError
from models import BinaryOperatorNode, NumberNode, UnaryOperatorNode

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

    def success(self, node):
        self.node = node 
        return self
    
    def failure(self, error_message):
        self.error = error_message
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (TT_PLUS, TT_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOperatorNode(token, factor)) 

        elif token.type in (TT_INT, TT_FLOAT):
            result.register(self.advance())
            return result.success(NumberNode(token))

        elif token.type == TT_LPAREN:
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type != TT_RPAREN:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected ')'"
                    )
                )
            result.register(self.advance())
            return result.success(expression)

        return result.failure(InvalidSyntaxError(
                token.pos_start, token.pos_end,
                f"Expected int or float, got '{token}'")
            )

    def term(self):
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))
        

    def expression(self):
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))


    def binary_operation(self, func, ops):
        result = ParseResult()
        left = result.register(func())
        if result.error:
            return result
        while self.current_token.type in ops:
            token = self.current_token
            result.register(self.advance())
            right = result.register(func())
            if result.error:
                return result
            left = BinaryOperatorNode(left, token, right)
        return result.success(left)

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected '+', '-', '*', '/', got '{self.current_token}'"
                )
            )
        return res
