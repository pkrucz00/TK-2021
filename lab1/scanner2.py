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

tokens = (
          'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
          'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
          'LE', 'GE', 'NEQ', 'EQ',
          'ID',
          'INT',
          'FLOAT',
          'STRING') + list(reserved.values())



literals = "+-*/=<>()[]{}:',;"

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

#TUTAJ ZNALEZIONE https://titanwolf.org/Network/Articles/Article?AID=0c88c627-a452-4d9b-8a7b-af6d83e71969#gsc.tab=0

def t_ID(t):
    r"[a-zA-Z_]\w*"
    t.type = reserved.get(t.value, 'ID')
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
