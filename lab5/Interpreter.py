import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy

sys.setrecursionlimit(10000)

binOps = {
    "+": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),
}

binOpsMatrix = {
    ".+": (lambda x, y: numpy.add(x, y)),
    ".-": (lambda x, y: numpy.subtract(x, y)),
    ".*": (lambda x, y: numpy.multiply(x, y)),
    "./": (lambda x, y: numpy.divide(x, y)),
    "+": (lambda x, y: numpy.matrix(x) + numpy.matrix(y)),
    "-": (lambda x, y: numpy.matrix(x) - numpy.matrix(y)),
    "*": (lambda x, y: numpy.matrix(x) * numpy.matrix(y)),
    "/": (lambda x, y: numpy.matrix(x) / numpy.matrix(y)),

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
    "+=": (lambda x, y: x + y),
    "-=": (lambda x, y: x - y),
    "*=": (lambda x, y: x * y),
    "/*": (lambda x, y: x / y),
}

assignOpsMatrix = {
    "+=": (lambda x, y: numpy.matrix(x) + numpy.matrix(y)),
    "-=": (lambda x, y: numpy.matrix(x) - numpy.matrix(y)),
    "*=": (lambda x, y: numpy.matrix(x) * numpy.matrix(y)),
    "/=": (lambda x, y: numpy.matrix(x) / numpy.matrix(y)),
}


class Interpreter(object):
    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

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
        return [elem.accept(self) for elem in node.vector]

    @when(AST.Matrix)
    def visit(self, node):
        return [[elem.accept(self) for elem in vector] for vector in node.matrix]

    @when(AST.MatrixFunction)
    def visit(self, node):
        if node.func == "eye":
            return numpy.eye(node.value)
        elif node.func == "ones":
            return numpy.ones(node.value)
        else:
            return numpy.zeros(node.value)

    @when(AST.Transposition)
    def visit(self, node):
        matrix = self.matrix.accept(self)
        return numpy.transpose(matrix)

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

    @when(AST.BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        pass
    #
    #

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

