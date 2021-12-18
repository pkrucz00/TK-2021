import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

binOps = {
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),
}

binOpsMatrix = {
    ".+": (lambda x, y: x + y),
    ".-": (lambda x, y: x - y),
    ".*": (lambda x, y: x * y),
    "./": (lambda x, y: x / y),
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: np.dot(x, y)),
    "/": (lambda x, y: np.linalg.solve(y, x)),
}

binOpsString = {
    "+": (lambda x, y: x + y),
    "*": (lambda x, y: x * y)
}

compOps = {
    ">": (lambda x, y: x > y),
    "<": (lambda x, y: x < y),
    ">=": (lambda x, y: x >= y),
    "<=": (lambda x, y: x <= y),
    "==": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
}

assignOps = {
    "+=": binOps["+"],
    "-=": binOps["-"],
    "*=": binOps["*"],
    "/*": binOps["/"],
}

assignOpsMatrix = {
    "+=": binOpsMatrix["+"],
    "-=": binOpsMatrix["-"],
    "*=": binOpsMatrix["*"],
    "/=": binOpsMatrix["/"],
}


class Interpreter(object):
    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Num)
    def visit(self, node):
        if isinstance(node.value, int):
            return int(node.value)
        else:
            return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Return)
    def visit(self, node):
        return node.val.accept(self)

    @when(AST.Error)
    def visit(self, node):
        pass

    @when(AST.Cond)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.rel_op
        return compOps[op](r1, r2)

    @when(AST.Vector)
    def visit(self, node):
        return np.array([elem.accept(self) for elem in node.vector])

    @when(AST.Matrix)
    def visit(self, node):
        return np.array([vector.accept(self) for vector in node.matrix])

    @when(AST.MatrixFunction)
    def visit(self, node):
        if node.func == "eye":
            return np.eye(node.value)
        elif node.func == "ones":
            return np.ones(node.value)
        else:
            return np.zeros((node.value, node.value))

    @when(AST.Transposition)
    def visit(self, node):
        matrix = node.matrix.accept(self)
        return np.transpose(matrix)

    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            self.memoryStack.push(Memory("if"))
            r = node.instruction.accept(self)
            self.memoryStack.pop()
            return r

    @when(AST.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            self.mamoryStack.push(Memory("if"))
            r = node.instruction.accept(self)
            self.memoryStack.pop()
            return r
        else:
            self.memoryStack.push(Memory("else"))
            r = node.else_instruction.accept(self)
            self.memoryStack.pop()
            return r

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op = node.bin_op
        if self.is_string(r1) or self.is_string(r2) and op in binOpsString:
            return binOpsString[op](r1, r2)
        elif self.is_num(r1) and self.is_num(r2) and op in binOps:
            return binOps[op](r1, r2)
        elif self.is_multidimentional(r1) or self.is_multidimentional(r2) and op in binOpsMatrix:
            return binOpsMatrix[op](r1, r2)
        else:
            raise BinaryOperationException(f"Could not find fitting binary operation for {r1} {op} {r2}")

    def is_num(self, val):
        return isinstance(val, int) or isinstance(val, float)

    def is_string(self, val):
        return isinstance(val, str)

    @when(AST.AssignOperation)
    def visit(self, node):
        var = node.variable
        expression_val = node.expression.accept(self)
        op = node.op
        if isinstance(var, AST.MatrixElement):
            self.assign_matrix_element(var, expression_val, op)
        elif isinstance(var, AST.VectorElement):
            self.assign_vector_element(var, expression_val, op)
        else:
            self.assign_variable(var.id, expression_val, op)

    def assign_matrix_element(self, matrix_elem_node, expression_val, op):
        matrix_id, x, y = matrix_elem_node.id.id, matrix_elem_node.index_x, matrix_elem_node.index_y
        matrix = self.memoryStack.get(matrix_id)
        if self.check_matrix_and_value_type(matrix[x][y], expression_val):
            raise AssignmentException()

        if op == "=":
            matrix[x][y] = expression_val
        else:
            curr_value = matrix_elem_node.accept(self)
            new_value = assignOps[op](curr_value, expression_val)
            matrix[x][y] = new_value

    def assign_vector_element(self, vector_elem_node, expression_val, op):
        vector_id, x = vector_elem_node.id, vector_elem_node.index
        vector = self.memoryStack.get(vector_id)
        if self.check_matrix_and_value_type(vector[x], expression_val):
            raise AssignmentException()

        if op == "=":
            vector[x] = expression_val
        else:
            curr_value = vector_elem_node.accept(self)
            new_value = assignOps[op](curr_value, expression_val)
            vector[x] = new_value

    def assign_variable(self, id, expression_value, op):
        if op == "=":
            if self.memoryStack.get(id) is not None:
                self.memoryStack.set(id, expression_value)
            else:
                self.memoryStack.insert(id, expression_value)
        else:
            curr_value = self.memoryStack.get(id)
            new_value = assignOps[op](curr_value, expression_value) \
                    if self.is_multidimentional(expression_value) \
                    else assignOps[op](curr_value, expression_value)
            self.memoryStack.set(id, new_value)


    def is_multidimentional(self, obj):
        return isinstance(obj, np.ndarray)


    def check_matrix_and_value_type(self, matrix_elem, value):
        return type(matrix_elem) == type(value)   # zakładamy, że w macierzy znajdują się dobre wartości

    @when(AST.ID)
    def visit(self, node):
        var_name = node.id
        return self.memoryStack.get(var_name)

    @when(AST.VectorElement)
    def visit(self, node):
        vector = node.id.accept(self)
        index = node.index.accept(self)
        return vector[index]

    @when(AST.MatrixElement)
    def visit(self, node):
        matrix = node.id.accept(self)
        x = node.index_x
        y = node.index_y
        return matrix[x, y]

    # simplistic while loop interpretation
    @when(AST.WhileLoop)
    def visit(self, node):
        self.memoryStack.push(Memory("while"))

        while node.condition.accept(self):
            node.instruction.accept(self)

        self.memoryStack.pop()

    @when(AST.ForLoop)
    def visit(self, node):
        self.memoryStack.push(Memory("for"))
        loop_range = node.f_range.accept(self)
        self.memoryStack.insert(node.l_id.id, None)
        for iter in loop_range:
            self.memoryStack.set(node.l_id.id, iter)
            node.instruction.accept(self)

        self.memoryStack.pop()

    @when(AST.Range)
    def visit(self, node):
        start_val = node.start.accept(self)
        end_val = node.end.accept(self)
        return range(start_val, end_val + 1)

    @when(AST.Print)
    def visit(self, node):
        print(node.print_vars.accept(self))

    @when(AST.PrintVals)
    def visit(self, node):
        return " ".join([str(print_val.accept(self)) for print_val in node.vals])
