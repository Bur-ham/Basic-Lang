class Position:
    def __init__(self, index, line, column, filename, filetext):
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.filetext = filetext

    def advance(self, current_char = None):
        self.index += 1
        self.column += 1
        if current_char == '\n':
            self.line += 1
            self.column = 0
    
    def copy(self):
        return Position(self.index, self.line, self.column, self.filename, self.filetext)

class Token:
    def __init__(self, type_, value=None, pos_start: Position = None, pos_end: Position = None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance(value)

        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f"{self.token}"


class BinaryOperatorNode:
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

        self.pos_start = self.left.pos_start
        self.pos_end = self.right.pos_end


    def __repr__(self):
        return f"({self.left}, {self.op_token}, {self.right})"

class UnaryOperatorNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"({self.op_token}, {self.right})"


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def __repr__(self):
        return f"{self.value}"

    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        return Number(self.value + other.value)
    
    def subtracted_from(self, other):
        return Number(self.value - other.value)
    
    def multiplied_by(self, other):
        return Number(self.value * other.value)
    
    def divided_by(self, other):
        return Number(self.value / other.value)
    
