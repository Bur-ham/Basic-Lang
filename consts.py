import string

###############################################################################
# Digits
###############################################################################

DIGITS = string.digits + '.'


###############################################################################
# TOKEN TYPES
###############################################################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

symbol_table = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '(': 'LPAREN',
    ')': 'RPAREN',
}
