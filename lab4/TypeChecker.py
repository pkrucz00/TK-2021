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

    def visit_Num(self, node):
        value = node.value
        return "int" if isinstance(value, int) else "float"


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
            self.add_error(node.line, "Wrong type in binary expression")
            return None

    def visit_Cond(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        rel_op = node.rel_op
        result_type = ttype[rel_op][str(type_left)][str(type_right)]
        if result_type is not None:
            return result_type
        else:
            self.add_error(node.line, "Wrong type in condition")
            return None

    def visit_AssignOperation(self, node):
        type_expr = self.visit(node.expression)
        op = node.op
        if op == '=':
            self.symbol_table.put(node.variable.id, type_expr)

        else:
            type_var = self.visit(node.variable)
            result_type = ttype[op][str(type_var)][str(type_expr)]
            if result_type is not None:
                if result_type == 'vector':
                    if isinstance(type_var, VectorType) and isinstance(type_expr, VectorType):
                        if type_var.size != type_expr.size:
                            self.add_error(node.line, "Wrong size of vectors in expression")
                            return None
                return result_type
            else:
                self.add_error(node.line, "Wrong type in assign operation")
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

    def visit_Print(self, node):
        self.visit(node.print_vars)

    def visit_Matrix(self, node):
        vectors = [self.visit(vector) for vector in node.matrix]

        vector_lengths = [len(vector.vector) for vector in node.matrix]
        are_vector_lengths_the_same = len(set(vector_lengths)) == 1
        if not are_vector_lengths_the_same:
            self.add_error(node.line, "Vectors in the matrix have inconsistent lengths")

        vector_types = [vector.type for vector in vectors]
        are_vector_types_the_same = len(set(vector_types)) == 1
        if not are_vector_types_the_same:
            self.add_error(node.line, "Vector types in the matrix are inconsistent")

        vector_dimensions = [vector.dimension for vector in vectors]
        are_vectors_one_dimensional = all(
            [dimension == 1 for dimension in vector_dimensions])
        if not are_vectors_one_dimensional:
            self.add_error(node.line, "Vector dimensions are not one dimensional")

        if not (are_vectors_one_dimensional and are_vector_types_the_same and are_vector_lengths_the_same):
            return None

        matrix_size = [len(vector_lengths), vector_lengths[0]]
        matrix_type = vector_types[0]

        return VectorType(matrix_size, matrix_type, 2)

    def visit_Vector(self, node):
        self.visit(node.vector)

        types = [self.visit(vector_num) for vector_num in node.vector]
        is_filled_with_int = \
            reduce(lambda acc, vect_elem_type:
                   vect_elem_type == "int" and acc,
                   [True] + types)
        is_filled_with_float = \
            reduce(lambda acc, vect_elem_type:
                    vect_elem_type == "float" and acc,
                    [True] + types)

        if not is_filled_with_float and not is_filled_with_int:
            self.add_error(node.line, "Not numeric values in vector")
            return None

        vector_type = "int" if is_filled_with_int else "float"
        return VectorType([len(node.vector)], vector_type, 1)

    def visit_PrintVals(self, node):
        self.visit(node.vals)


    def visit_String(self, node):
        return "string"

    def visit_Variable(self, node):
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
        if isinstance(node.value, int):
            return VectorType([node.value, node.value], 'int', 2)
        else:
            self.add_error(node.line, "Wrong type in matrix function")
            return None

    def visit_Transposition(self, node):
        vector_type = self.visit(node.matrix)
        if not isinstance(VectorType, vector_type):
            self.add_error(node.line, "Wrong type in transposition")

        if vector_type.dimension == 1:
            return VectorType([1, vector_type.size], vector_type.type, 2)
        elif vector_type.dimension == 2:
            return VectorType(reversed(vector_type.size), vector_type.type, 2)
        else:
            self.add_error(node.line, "Wrong dimension in transposition")
            return None

    def visit_Uminus(self, node):
        type_expression = self.visit(node.expression)
        type = ttype["-"][type_expression][None]
        if not type:
            self.add_error(node.line, "Wrong type in unary minus")
            return None

        return type

    def visit_ID(self, node):
        return self.symbol_table.get(node.id)

    def visit_VectorElement(self, node):
        index = node.index
        if not isinstance(index, int):
            self.add_error(node.line, "Wrong type of index")
            return None

        variable_symbol = self.symbol_table.get(node.id)
        vector_type = variable_symbol
        if vector_type is None or not isinstance(vector_type, VectorType):
            self.add_error(node.line, f"Vector {node.id} uninitialized or of wrong type")
            return None

        if vector_type.dimension != 1:
            self.add_error(node.line, "Wrong dimension for vector element")
            return None
        elif not (0 <= index < vector_type.size):
            self.add_error(node.line, "Index out of bounds")
            return None

        return vector_type.type
        # sprawdzenie, czy index jest poza zakresem
        # return self.symbol_table.do_something(node)    sprawdzić typ w tablicy symboli

    def visit_MatrixElement(self, node):
        x, y = node.index_x, node.index_y
        if not (isinstance(x, int) and isinstance(y, int)):
            self.add_error(node.line, "Wrong type of index in matrix element")
            return None

        variable_symbol = self.visit(node.id)
        matrix_type = variable_symbol.type
        if matrix_type is None or not isinstance(matrix_type, VectorType):
            self.add_error(node.line, f"Vector {node.id.id} uninitialized or of wrong type")
            return None

        if matrix_type.dimension != 2:
            self.add_error(node.line, "Wrong dimension for a matrix element")
            return None

        max_x, max_y = matrix_type.size[0], matrix_type.size[1]
        are_x_and_y_in_bounds = 0 <= x < max_x and 0 <= y < max_y
        if not are_x_and_y_in_bounds:
            self.add_error(node.line, "Index out of bounds")
            return None

        return matrix_type.type
