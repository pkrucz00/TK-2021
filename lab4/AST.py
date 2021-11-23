class Node(object):
    pass


class Instructions(Node):
    def __init__(self, new_instruction, instructions=None):
        self.instructions = instructions.instructions if instructions else []
        self.instructions.append(new_instruction)


class BinExpr(Node):
    def __init__(self, bin_op, left, right):
        self.bin_op = bin_op
        self.left = left
        self.right = right


class Cond(Node):
    def __init__(self, rel_op, left, right):
        self.rel_op = rel_op
        self.left = left
        self.right = right


class AssignOperation(Node):
    def __init__(self, variable, op, expression):
        self.variable = variable
        self.op = op
        self.expression = expression


class If(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class IfElse(Node):
    def __init__(self, condition, instruction, else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class ForLoop(Node):
    def __init__(self, l_id, f_range, instruction):
        self.l_id = l_id
        self.f_range = f_range
        self.instruction = instruction


class Break(Node):
    def __init__(self):
        pass


class Continue(Node):
    def __init__(self):
        pass


class Return(Node):
    def __init__(self, val):
        self.val = val


class Print(Node):
    def __init__(self, print_vars):
        self.print_vars = print_vars


class Matrix(Node):
    def __init__(self, new_vector, matrix=None):
        self.matrix = matrix.matrix.copy() if matrix else []
        self.matrix.append(new_vector)


class Vector(Node):
    def __init__(self, new_elem, vector=None):
        self.vector = vector.vector.copy() if vector else []
        self.vector.append(new_elem)


class PrintVals(Node):
    def __init__(self, new_val, vals=None):
        self.vals = vals.vals.copy() if vals else []   #TODO sprawdzić, czy program wywala sie, kiedy nie kopiujemy
        self.vals.append(new_val)


class Num(Node):           # ta klasa powinna zastąpić 2 (poniżej zakomentowane) klasy
    def __init__(self, value):
        self.value = value

# class IntNum(Node):
#     def __init__(self, value):
#         self.value = value
#
#
# class FloatNum(Node):
#     def __init__(self, value):
#         self.value = value
#

class String(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class MatrixFunction(Node):
    def __init__(self, func, value):
        self.func = func
        self.value = value


class Transposition(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Uminus(Node):
    def __init__(self, expression):
        self.expression = expression


class ID(Node):
    def __init__(self, id):
        self.id = id


class VectorElement(Node):
    def __init__(self, id, index):
        self.id = id
        self.index = index


class MatrixElement(Node):
    def __init__(self, id, index_x, index_y):
        self.id = id
        self.index_x = index_x
        self.index_y = index_y


class Error(Node):
    def __init__(self):
        pass

class Empty(Node):
    def __init__(self):
        pass
