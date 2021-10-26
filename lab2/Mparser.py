#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

start = program

precedence = (
    # to fill ...
    ("left", '+', '-'),
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction block
                    | instruction
                    | block"""


def p_instruction(p):
    """instruction : statement ";" """


def p_block(p):
    """block: "{" instructions_opt "}" """


def p_statement(p):
    """statement : assignment
                  | loop_statement
                  | if_statement
                  | print_statement"""


def p_assignment(p):
    """ assignment: variable "=" expression
                  | variable ADDASSIGN expression
                  | variable SUBASSIGN expression
                  | variable MULASSIGN expression
                  | variable DIVASSIGN expression"""


def p_variable(p):
    """ variable: ID
                | element"""


def p_element(p):
    """ element: vector_element
               | matrix_element"""


def p_vector_element(p):
    # możemy przedyskutować, czy potrzebny jest podział na "vector" i "matrix",
    # czy może "matrix" to po prostu wiele obiektów typu "vector"
    """ vector_element: ID "[" INT "]" """


def p_matrix_element(p):
    """ matrix_element: ID "[" INT "," INT "]" """


def p_expression(p):
    """ expression: math_expression
                   | matrix_expression
                   | matrix_function"""


def p_print_statement(p):
    """ print_statement: PRINT STRING"""

parser = yacc.yacc()

