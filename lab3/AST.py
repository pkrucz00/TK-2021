class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


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


class While(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class For(Node):
    def __init__(self, l_id, f_range, instruction):
        self.l_id = l_id
        self.f_range = f_range
        self.instruction = instruction


class If(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class If_else(Node):
    def __init__(self, condition, instruction, else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
