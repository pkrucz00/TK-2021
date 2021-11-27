#!/usr/bin/python

from SymbolTable import SymbolTable


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

class Error:
    def __init__(self, line_number, error_message):
        self.line_number = line_number
        self.error_message = error_message


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = None
        self.errors = None

    def init_visit(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def print_errors(self):
        for error in self.errors:
            print(f'Line [{error.line_number}]: {error.error_message}')

    def visit_Instructions(self, node):
        self.init_visit()
        for instruction in node.instructions:
            self.visit(instruction)
        self.print_errors()

    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        op = node.op
        # type check
        # return bin_expr_type  TODO fill when ttype is added

    def visit_Cond(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        rel_op = node.rel_op
        # type_checking

    def visit_AssignOperation(self, node):
        type_var = self.visit(node.variable)
        type_expr = self.visit(node.expression)
        op = node.op
        # type_checking
        # returning type

    #Poniższe "Instrukcje blokowe" będą zapewne potrzebowały,
    # aby jakoś zaznaczyć, że w nie wchodzimy.
    # Inaczej trudno będzie sprawdzić, czy break i continue są dobrze użyte
    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)

    def visit_IfElse(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)
        self.visit(node.else_instruction)

    def visit_WhileLoop(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)

    def visit_ForLoop(self, node):
        self.visit(node.l_id)
        #sprawdzenie, czy l_id nie jest już zajęte
        self.visit(node.f_range)
        self.instruction(node.instruction)

    def visit_Break(self, node):
        # check scope
        pass

    def visit_Continue(self, node):
        # check scope
        pass

    def visit_Return(self, node):
        return self.visit(node.val)

    #Tutaj chyba nie trzeba nic robić -
    # nasz kompilator nie patrzy na typy drukowanych zmiennych.
    # Nie ma potrzeby zwracania typu, bo i jaki miałby on być.
    def visit_Print(self, node):
        pass

    #sprawdzanie, czy macierz jest kwadratowa zapewne też
    # powinno być jakoś zrobione z pomocą tablicy symboli
    def visit_Matrix(self, node):
        self.visit(node.matrix)
        # check vector length integrity

    def visit_Vector(self, node):
        self.visit(node.vector)

    # to samo co przy visit_Print
    def visit_PrintVals(self, node):
        pass

    def visit_Num(self, node):
        value = node.value
        # być może tutaj bedzie wpis w tablicy symboli
        return "int" if isinstance(value, int) else "float"

    def visit_String(self, node):
        #być może wpis w tablicy symboli
        return "string"

    def visit_Variable(self, node):
        # być może wpis w tablicy symboli
        return self.visit(node.name)

    def visit_Range(self, node):
        type_start = self.visit(node.start)
        type_end = self.visit(node.end)
        # type_check

    def visit_MatrixFunction(self, node):
        type_value = self.visit(node.value)
        # type_check

    def visit_Transposition(self, node):
        type_matrix = self.visit(node.matrix)
        # type_check
        return type_matrix

    def visit_Uminus(self, node):
        type_expression = self.visit(node.expression)
        # type_check
        return type_expression

    def visit_ID(self, node):
        # return self.symbol_table.do_something(node)    sprawdzić typ w tablicy symboli
        return None

    def visit_VectorElement(self, node):
        type_index = self.visit(node.index)
        # type_check
        # sprawdzenie, czy index jest poza zakresem
        # return self.symbol_table.do_something(node)    sprawdzić typ w tablicy symboli

    def visit_MatrixElement(self, node):
        type_index_x = self.visit(node.index_x)
        type_index_y = self.visit(node.index_y)
        #type_check
        # sprawdzenie, czy indeksy są poza zakresem
        # return self.symbol_table.do_something(node)      sprawdzenie typu w tablicy symboli


