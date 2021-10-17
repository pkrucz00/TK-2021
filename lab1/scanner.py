import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
          'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
          'LE', 'GE', 'NEQ', 'EQ',
          'ID',
          'INT', 'FLOAT', 'STRING']\
         + list(reserved.values())

literals = "+-*/=<>()[]{}:',;"

'''
O ile dobrze rozumiem, to taką składnię można używać,
dopóki nie mówimy o słowach kluczowych, tak?
'''
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LE = r'<='
t_GE = r'>='
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'((\.\d+)|(\d+\.\d*))([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'"([^"]+|\\"|\\\\)*"'  # Nie rozumiem tego :c. Czy można dać tutaj np. r'".*"?
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# O ile rozumiem, to błąd powinien wyrzucać wyjątek,
# ale wtedy analizator musiałby się zatrzymać,
# więc pewnie zostawiamy to w ten sposób, żeby pokazać,
# że nasz kod potrafi również resztę testu przemielić?
# I tak, wiem, że tak było na stronie dr Kuty:)
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Nie rozumiem, co robi ta funkcja
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def lexer():
    return lex.lex()