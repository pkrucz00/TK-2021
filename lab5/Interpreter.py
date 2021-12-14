import AST
import SymbolTable
from Memory import *
from Exceptions import  *
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
            return np.zeros(node.value)

    @when(AST.Transposition)
    def visit(self, node):
        matrix = self.matrix.accept(self)
        return np.transpose(matrix)

    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            self.mamoryStack.push(Memory("if"))
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
        if isinstance(r1, AST.Num) and isinstance(r2, AST.Num):
            return binOps[op](r1, r2)
        else:
            return binOpsMatrix[op](r1, r2)

    @when(AST.AssignOperation)
    def visit(self, node):
        left_side_name = node.variable.id
        right_side = node.expression.accept(self)
        op = node.op
        if op == "=":
            self.memoryStack.insert(left_side_name, right_side)
        elif op in assignOps:
            left_side_value = self.memoryStack.get(left_side_name)
            # if isinstance(right_side, AST.Vector) or isinstance(right_side, AST.Matrix):
            new_value = assignOpsMatrix[op](left_side_value, right_side)
            self.memoryStack.set(left_side_name, new_value)
    #

    @when(AST.ID)
    def visit(self, node):
        var_name = node.id
        return self.memoryStack.get(var_name)

    # simplistic while loop interpretation
    @when(AST.WhileLoop)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

    @when(AST.Print)
    def visit(self, node):
        print(node.print_vars.accept(self))

    @when(AST.PrintVals)
    def visit(self, node):
        return "".join([str(print_val.accept(self)) for print_val in node.vals])




