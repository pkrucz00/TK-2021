import ply.yacc as yacc
import scanner
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


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : empty"""


def p_instructions(p):
    """instructions : instruction
                    | instruction instructions"""


def p_instruction(p):
    """instruction : assignment ';'
                | statement ';'
                | '{' instructions '}'
                """


def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IFX """


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction """


def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction """


def p_instruction_for(p):
    """instruction : FOR var '=' range instruction """


def p_range(p):
    """range : expression ':' expression """


def p_condition(p):
    """condition : expression EQ expression
                 | expression NEQ expression
                 | expression LE expression
                 | expression GE expression
                 | expression '<' expression
                 | expression '>' expression """


def p_assignment_op(p):
    """assignment_op : MULASSIGN
                   | DIVASSIGN
                   | SUBASSIGN
                   | ADDASSIGN
                   | '=' """


def p_assignment(p):
    """assignment : var assignment_op expression
                | matrix_element assignment_op expression
                | vector_element assignment_op expression """


def p_matrix_function(p):
    """matrix_function : matrix_function_name '(' INT ')' """


def p_matrix_function_name(p):
    """matrix_function_name : EYE
                            | ONES
                            | ZEROS """


def p_matrix(p):
    """matrix : '[' vectors ']' """


def p_vectors(p):
    """vectors : vectors ',' vector
               | vector """


def p_vector(p):
    """vector : '[' variables ']' """


def p_variables(p):
    """variables : variables ',' variable
                 | variable """


def p_variable(p):
    """variable : number
                 | var
                 | element """


def p_element(p):
    """ element : vector_element
               | matrix_element"""


def p_vector_element(p):
    """ vector_element : ID "[" INT "]" """


def p_matrix_element(p):
    """ matrix_element : ID "[" INT "," INT "]" """


def p_var(p):
    """var : ID """


def p_number(p):
    """number : INT
             | FLOAT """


def p_string(p):
    """string : STRING """


def p_bin_expression(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""


def p_expression(p):
    """expression : num_expression
            | matrix
            | matrix_function
            | uminus
            | transposition
            | matrix_element
            | vector_element """


def p_num_expression(p):
    """num_expression : number
                      | var """


def p_uminus(p):
    """uminus : '-' expression %prec UMINUS """


def p_transposition(p):
    """transposition : expression "'" """


def p_break_statement(p):
    """statement : BREAK"""


def p_continue_statement(p):
    """statement : CONTINUE"""


def p_return_statement(p):
    """statement : RETURN expression """


def p_print_statement(p):
    """statement : PRINT print_vals """


def p_print_vals(p):
    """print_vals : print_vals ',' print_val
                  | print_val """


def p_print_val(p):
    """print_val : string
                 | expression"""


parser = yacc.yacc()