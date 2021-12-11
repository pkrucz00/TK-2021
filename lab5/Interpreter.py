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
    #
    #

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

