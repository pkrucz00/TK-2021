#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

start = 'program'

precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("nonassoc", '='),
    ("nonassoc", "INT"),
    ("nonassoc", "FLOAT"),
    ("nonassoc", 'ADDASSIGN', 'SUBASSIGN'),
    ("nonassoc", 'MULASSIGN', 'DIVASSIGN'),
    ("left", '+', '-', 'DOTADD', 'DOTSUB'),
    ("left", '*', '/', 'DOTMUL', "DOTDIV")
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
    """instructions : instructions instruction
                    | instruction
                    | "{" instructions "}" """


def p_instruction(p):
    """instruction : statement ";" """


def p_instruction_if(p):
    """ instruction : IF '(' condition ')' instructions %prec IFX """


def p_instruction_if_else(p):
    """ instruction : IF '(' condition ')' instructions ELSE instructions """


def p_instruction_for(p):
    """ instruction : FOR ID '=' range instructions """


def p_instruction_while(p):
    """ instruction : WHILE '(' condition ')' instructions """


def p_range(p):
    """ range : expression ':' expression """


def p_condition(p):
    """ condition : expression EQ expression
                  | expression NEQ expression
                  | expression LE expression
                  | expression GE expression
                  | expression '<' expression
                  | expression '>' expression """


def p_statement(p):
    """statement : assignment
                  | print_statement"""


def p_assignment(p):
    """ assignment : variable "=" expression
                   | variable "=" matrix_function
                   | variable "=" matrix
                   | variable ADDASSIGN expression
                   | variable SUBASSIGN expression
                   | variable MULASSIGN expression
                   | variable DIVASSIGN expression"""


def p_matrix_function(p):
    """ matrix_function : matrix_function_name "(" INT ")" """


def p_matrix_function_name(p):
    """ matrix_function_name : ZEROS
                             | ONES
                             | EYE """


def p_matrix(p):
    """ matrix : "[" vectors "]" """


def p_vectors(p):
    """ vectors : vectors "," vector
                | vector """


def p_vector(p):
    """ vector : "[" variables "]" """


def p_variables(p):
    """ variables : variables "," variable
                  | variable """


def p_variable(p):
    """ variable : ID
                 | element
                 | number """


def p_element(p):
    """ element : vector_element
               | matrix_element"""


def p_vector_element(p):
    """ vector_element : ID "[" INT "]" """


def p_matrix_element(p):
    """ matrix_element : ID "[" INT "," INT "]" """


def p_expression(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '*' expression
                   | expression '/' expression
                   | expression DOTADD expression
                   | expression DOTSUB expression
                   | expression DOTMUL expression
                   | expression DOTDIV expression
                   | expression "'"
                   | "-" expression
                   | "(" expression ")"
                   | variable """


def p_number(p):
    """ number : INT
               | FLOAT """


def p_print_statement(p):
    """ print_statement : PRINT printables """


def p_printables(p):
    """ printables : printables "," printable
                   | printable """


def p_printable(p):
    """ printable : STRING
                  | variable """


def p_break_statement(p):
    """ statement : BREAK """


def p_continue_statement(p):
    """ statement : CONTINUE """


def p_return_statement(p):
    """ statement : RETURN variable """


parser = yacc.yacc()

