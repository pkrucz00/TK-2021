import ply.yacc as yacc
import scanner
import AST

tokens = scanner.tokens

start = 'program'
precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', '<', '>', 'GE', 'LE', 'EQ', 'NEQ'),
    ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
    ('left', '+', '-'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/'),
    ('left', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('left', "'"),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_empty(p):
    """ empty :"""
    p[0] = AST.Empty()


def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]


def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = p[1]


def p_instructions_opt_2(p):
    """instructions_opt : empty"""
    p[0] = p[1]


def p_instructions(p):
    """instructions : instruction
                    | instructions instruction"""
    if len(p) == 2:
        p[0] = AST.Instructions(p[1])
    elif len(p) == 3:
        p[0] = AST.Instructions(p[2], p[1])


def p_instruction(p):
    """instruction : assignment ';'
                | statement ';'
                | '{' instructions '}'
                """
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
    p[0].line = p.lexer.lineno


def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IFX """
    p[0] = AST.If(p[3], p[5])
    p[0].line = p.lexer.lineno


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction """
    p[0] = AST.IfElse(p[3], p[5], p[7])
    p[0].line = p.lexer.lineno

def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction """
    p[0] = AST.WhileLoop(p[3], p[5])
    p[0].line = p.lexer.lineno

def p_instruction_for(p):
    """instruction : FOR var '=' range instruction """
    p[0] = AST.ForLoop(p[2], p[4], p[5])
    p[0].line = p.lexer.lineno

def p_range(p):
    """range : expression ':' expression """
    p[0] = AST.Range(p[1], p[3])
    p[0].line = p.lexer.lineno

def p_condition(p):
    """condition : expression EQ expression
                 | expression NEQ expression
                 | expression LE expression
                 | expression GE expression
                 | expression '<' expression
                 | expression '>' expression """
    p[0] = AST.Cond(p[2], p[1], p[3])
    p[0].line = p.lexer.lineno

def p_assignment_op(p):
    """assignment_op : MULASSIGN
                   | DIVASSIGN
                   | SUBASSIGN
                   | ADDASSIGN
                   | '=' """
    p[0] = p[1]


def p_assignment(p):
    """assignment : var assignment_op expression
                | matrix_element assignment_op expression
                | vector_element assignment_op expression """
    p[0] = AST.AssignOperation(p[1], p[2], p[3])


def p_matrix_function(p):
    """matrix_function : EYE '(' INT ')'
                       | ONES '(' INT ')'
                       | ZEROS '(' INT ')' """
    p[0] = AST.MatrixFunction(p[1], p[3])
    p[0].line = p.lexer.lineno


def p_matrix(p):
    """matrix : '[' vectors ']' """
    p[0] = p[2]


def p_vectors(p):
    """vectors : vectors ',' vector
               | vector """
    if len(p) == 4:
        p[0] = AST.Matrix(p[3], p[1])
    if len(p) == 2:
        p[0] = AST.Matrix(p[1])
    p[0].line = p.lexer.lineno


def p_vector(p):
    """vector : '[' variables ']' """
    p[0] = p[2]


def p_variables(p):
    """variables : variables ',' variable
                 | variable """
    if len(p) == 4:
        p[0] = AST.Vector(p[3], p[1])
    if len(p) == 2:
        p[0] = AST.Vector(p[1])
    p[0].line = p.lexer.lineno


def p_variable(p):
    """variable : number
                 | var
                 | element """
    p[0] = p[1]


def p_element(p):
    """ element : vector_element
               | matrix_element"""
    p[0] = p[1]


def p_vector_element(p):
    """ vector_element : var "[" INT "]" """
    p[0] = AST.VectorElement(p[1], p[3])
    p[0].line = p.lexer.lineno

def p_matrix_element(p):
    """ matrix_element : var "[" INT "," INT "]" """
    p[0] = AST.MatrixElement(p[1], p[3], p[5])
    p[0].line = p.lexer.lineno

def p_number(p):
    """number : INT
             | FLOAT """
    p[0] = AST.Num(p[1])
    p[0].line = p.lexer.lineno


def p_string(p):
    """string : STRING """
    p[0] = AST.String(p[1])
    p[0].line = p.lexer.lineno


def p_bin_expression(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])
    p[0].line = p.lexer.lineno

def p_expression(p):
    """expression : num_expression
            | matrix
            | matrix_function
            | vector
            | uminus
            | transposition
            | matrix_element
            | vector_element """
    p[0] = p[1]


def p_num_expression(p):
    """num_expression : number
                      | var """
    p[0] = p[1]


def p_var(p):
    """ var : ID """
    p[0] = AST.ID(p[1])
    p[0].line = p.lexer.lineno


def p_uminus(p):
    """uminus : '-' expression %prec UMINUS """
    p[0] = AST.Uminus(p[2])
    p[0].line = p.lexer.lineno


def p_transposition(p):
    """transposition : expression "'" """
    p[0] = AST.Transposition(p[1])
    p[0].line = p.lexer.lineno


def p_break_statement(p):
    """statement : BREAK"""
    p[0] = AST.Break()
    p[0].line = p.lexer.lineno


def p_continue_statement(p):
    """statement : CONTINUE"""
    p[0] = AST.Continue()
    p[0].line = p.lexer.lineno


def p_return_statement(p):
    """statement : RETURN expression """
    p[0] = AST.Return(p[2])
    p[0].line = p.lexer.lineno


def p_print_statement(p):
    """statement : PRINT print_vals """
    p[0] = AST.Print(p[2])
    p[0].line = p.lexer.lineno


def p_print_vals(p):
    """print_vals : print_vals ',' print_val
                  | print_val """
    if len(p) == 4:
        p[0] = AST.PrintVals(p[3], p[1])
    if len(p) == 2:
        p[0] = AST.PrintVals(p[1])
    p[0].line = p.lexer.lineno


def p_print_val(p):
    """print_val : string
                 | expression"""
    p[0] = p[1]


parser = yacc.yacc()