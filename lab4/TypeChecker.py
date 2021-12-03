#!/usr/bin/python

from SymbolTable import SymbolTable, VectorType, VariableSymbol
import AST
from collections import defaultdict
from functools import reduce

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['<', '>', '>=', '<=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['float']['float'] = 'float'
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'

for op in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['float']['float'] = 'float'
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['vector']['vector'] = 'vector'

for op in ['.+', '.-', '.*', './']:
    ttype[op]['vector']['vector'] = 'vector'
    ttype[op]['vector']['int'] = 'vector'
    ttype[op]['vector']['float'] = 'vector'
    ttype[op]['int']['vector'] = 'vector'
    ttype[op]['float']['vector'] = 'vector'

ttype['\'']['vector'][None] = 'vector'
ttype['-']['vector'][None] = 'vector'
ttype['-']['int'][None] = 'int'
ttype['-']['float'][None] = 'float'
ttype['+']['string']['string'] = 'string'


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

    def __str__(self):
        return f'Line [{self.line_number}]: {self.error_message}'


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, 'main')
        self.errors = None
        self.loop_checker = 0

    def init_visit(self):
        self.symbol_table = SymbolTable(None, 'main')
        self.errors = []
        self.loop_checker = 0

    def add_error(self, line, message):
        new_error = Error(line, message)
        self.errors.append(new_error)

    def print_errors(self):
        for error in self.errors:
            print(error)

    def visit_Instructions(self, node):
        self.init_visit()
        for instruction in node.instructions:
            self.visit(instruction)
        self.print_errors()

    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        op = node.bin_op

        type = ttype[op][str(type_left)][str(type_right)]
        if type is not None:
            if type == 'vector':
                if isinstance(type_left, VectorType) and isinstance(type_right, VectorType):
                    if type_left.size != type_right.size:
                        self.add_error(node.line, "Different sizes of vectors in binary expression")
                    elif type_left.type != type_right.type:
                        self.add_error(node.line, "Different types in binary expression")
            return type
        else:
            self.add_error(node.line, "Wrong type")
            return None

    def visit_Cond(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        rel_op = node.rel_op
        result_type = ttype[rel_op][str(type_left)][str(type_right)]
        if result_type is not None:
            return result_type
        else:
            self.add_error(node.line, "Wrong type")
            return None

    def visit_AssignOperation(self, node):
        type_var = self.visit(node.variable)
        type_expr = self.visit(node.expression)
        op = node.op
        if node.variable in self.symbol_table.var_dict:
            self.add_error(node.line, f"Variable '{node.variable}' already exists")

        if op == '=':
            self.symbol_table.put(node.variable.id, VariableSymbol(node.variable.id, type_expr))   # w obiekcie VariableSymbol powtarzamy informację o nazwie zmiennej. Po co?
        else:
            result_type = ttype[op][str(type_var)][str(type_expr)]
            if result_type is not None:
                if result_type == 'vector':
                    if isinstance(type_var, VectorType) and isinstance(type_expr, VectorType):
                        if type_var.size != type_expr.size:
                            self.add_error(node.line, "Wrong size")
                            return None
                return result_type
            else:
                self.add_error(node.line, "Wrong type")
                return None

    def visit_If(self, node):
        self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()

    def visit_IfElse(self, node):
        self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()
        if node.else_instruction:
            self.symbol_table.pushScope('else')
            self.visit(node.else_instruction)
            self.symbol_table.popScope()

    def visit_WhileLoop(self, node):
        self.loop_checker += 1
        self.symbol_table = self.symbol_table.pushScope('while')
        self.visit(node.condition)
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_checker -= 1

    def visit_ForLoop(self, node):
        self.loop_checker += 1
        self.symbol_table = self.symbol_table.pushScope('for')
        type = self.visit(node.f_range)
        self.symbol_table.put(node.l_id.name, VariableSymbol(node.l_id.name, type))
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_checker -= 1

    def visit_Break(self, node):
        if self.loop_checker == 0:
            self.add_error(node.line, "Break outside the loop")

    def visit_Continue(self, node):
        if self.loop_checker == 0:
            self.add_error(node.line, "Continue outside the loop")

    def visit_Return(self, node):
        return self.visit(node.val)

    # Tutaj chyba nie trzeba nic robić -
    # nasz kompilator nie patrzy na typy drukowanych zmiennych.
    # Nie ma potrzeby zwracania typu, bo i jaki miałby on być.
    def visit_Print(self, node):
        self.visit(node.print_vars)

    # sprawdzanie, czy macierz jest kwadratowa zapewne też
    # powinno być jakoś zrobione z pomocą tablicy symboli
    def visit_Matrix(self, node):
        self.visit(node.matrix)
        print(node.matrix)
        # check vector length integrity

    def visit_Vector(self, node):
        self.visit(node.vector)
        types = [self.visit(vector_num) for vector_num in node.vector]
        is_filled_with_nums = reduce(lambda vect_elem_type, acc: (vect_elem_type == "int" or vect_elem_type == "float") and acc, True, types)
        print(is_filled_with_nums)
        # self.symbol_table.put

    # to samo co przy visit_Print
    def visit_PrintVals(self, node):
        pass

    def visit_Num(self, node):
        value = node.value
        # być może tutaj bedzie wpis w tablicy symboli
        return "int" if isinstance(value, int) else "float"

    def visit_String(self, node):
        # być może wpis w tablicy symboli
        return "string"

    def visit_Variable(self, node):
        # być może wpis w tablicy symboli
        return self.visit(node.name)

    def visit_Range(self, node):
        type_start = self.visit(node.start)
        type_end = self.visit(node.end)

        if type_start != 'int':
            self.add_error(node.line, "Error in type start")
            return None
        if type_end != 'int':
            self.add_error(node.line, "Error in type end")
            return None
        return type_start

    def visit_MatrixFunction(self, node):
        type_value = self.visit(node.value)
        if type_value == 'int':
            return VectorType([node.value, node.value], 'int', 2)
        else:
            self.add_error(node.line, "Wrong type in matrix function")
            return None

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
        # type_check
        # sprawdzenie, czy indeksy są poza zakresem
        # return self.symbol_table.do_something(node)      sprawdzenie typu w tablicy symboli
