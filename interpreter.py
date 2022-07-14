from consts import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV
from models import Number

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_NumberNode(self, node):
        return Number(node.token.value).set_pos(node.token.pos_start, node.token.pos_end)

    def visit_BinaryOperatorNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op_token.type == TT_PLUS:
            result = left.added_to(right)
        elif node.op_token.type == TT_MINUS:
            result = left.subtracted_from(right)
        elif node.op_token.type == TT_MUL:
            result = left.multiplied_by(right)
        elif node.op_token.type == TT_DIV:
            result = left.divided_by(right)
            
        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOperatorNode(self, node):
        number = self.visit(node.node)

        if node.op_token.type == TT_MINUS:
            number = number.multiplied_by(Number(-1))
        
        return number.set_pos(node.pos_start, node.pos_end)