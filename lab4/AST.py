
class Node(object):
    def __init__(self):
        self.line = None


class Instructions(Node):
    def __init__(self, new_instruction, instructions=None):
        super().__init__()
        self.instructions = instructions.instructions if instructions else []
        self.instructions.append(new_instruction)


class BinExpr(Node):
    def __init__(self, bin_op, left, right):
        super().__init__()
        self.bin_op = bin_op
        self.left = left
        self.right = right


class Cond(Node):
    def __init__(self, rel_op, left, right):
        super().__init__()
        self.rel_op = rel_op
        self.left = left
        self.right = right


class AssignOperation(Node):
    def __init__(self, variable, op, expression):
        super().__init__()
        self.variable = variable
        self.op = op
        self.expression = expression


class If(Node):
    def __init__(self, condition, instruction):
        super().__init__()
        self.condition = condition
        self.instruction = instruction


class IfElse(Node):
    def __init__(self, condition, instruction, else_instruction):
        super().__init__()
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        super().__init__()
        self.condition = condition
        self.instruction = instruction


class ForLoop(Node):
    def __init__(self, l_id, f_range, instruction):
        super().__init__()
        self.l_id = l_id
        self.f_range = f_range
        self.instruction = instruction


class Break(Node):
    def __init__(self):
        super().__init__()


class Continue(Node):
    def __init__(self):
        super().__init__()


class Return(Node):
    def __init__(self, val):
        super().__init__()
        self.val = val


class Print(Node):
    def __init__(self, print_vars):
        super().__init__()
        self.print_vars = print_vars


class Matrix(Node):
    def __init__(self, new_vector, matrix=None):
        super().__init__()
        self.matrix = matrix.matrix.copy() if matrix else []
        self.matrix.append(new_vector)


class Vector(Node):
    def __init__(self, new_elem, vector=None):
        super().__init__()
        self.vector = vector.vector.copy() if vector else []
        self.vector.append(new_elem)


class PrintVals(Node):
    def __init__(self, new_val, vals=None):
        super().__init__()
        self.vals = vals.vals.copy() if vals else []
        self.vals.append(new_val)


class Num(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class String(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Variable(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name


class Range(Node):
    def __init__(self, start, end):
        super().__init__()
        self.start = start
        self.end = end


class MatrixFunction(Node):
    def __init__(self, func, value):
        super().__init__()
        self.func = func
        self.value = value


class Transposition(Node):
    def __init__(self, matrix):
        super().__init__()
        self.matrix = matrix


class Uminus(Node):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression


class ID(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id


class VectorElement(Node):
    def __init__(self, id, index):
        super().__init__()
        self.id = id
        self.index = index


class MatrixElement(Node):
    def __init__(self, id, index_x, index_y):
        super().__init__()
        self.id = id
        self.index_x = index_x
        self.index_y = index_y


class Error(Node):
    def __init__(self):
        super().__init__()


class Empty(Node):
    def __init__(self):
        super().__init__()

