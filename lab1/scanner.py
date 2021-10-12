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

tokens = ('ADD', 'SUB', 'MUL', 'DIV',  #OPERATORY BINARNE
          'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
          '=', '+=', '-=', '*=', '/=',
          '<', '>', '<=', '>=', '!=', '==',
          '(', ')', '[', ']', '{', '}',
          'RANGE', #OPERATOR ZAKRESU `:`
          "'",
          ',', ';',
          'ID',
          'INT',
          'FLOAT',
          'STRING') + list(reserved.values())






}
