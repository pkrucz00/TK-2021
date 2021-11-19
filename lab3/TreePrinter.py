import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @classmethod
    def make_indent(self, indent):
        return ''.join('| ' * indent)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for n in self.instructions:
            n.printTree(indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.bin_op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Cond)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.rel_op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignOperation)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.op)
        self.variable.printTree(indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(TreePrinter.make_indent(indent) + 'THEN')
        self.instruction.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(TreePrinter.make_indent(indent) + 'THEN')
        self.instruction.printTree(indent + 1)
        print(TreePrinter.make_indent(indent) + 'ELSE')
        self.else_instruction.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'WHILE')
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'FOR')
        self.l_id.printTree(indent + 1)
        self.f_range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("|    " * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("|    " * indent + "CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'RETURN')
        self.val.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'PRINT')
        self.print_vars.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'MATRIX')
        for el in self.matrix:
            el.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'VECTOR')
        for el in self.vector:
            el.printTree(indent + 1)

    @addToClass(AST.PrintVals)
    def printTree(self, indent=0):
        for el in self.vals:
            el.printTree(indent)

    @addToClass(AST.Num)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.name)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'RANGE')
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.func + str(self.value))

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + 'TRANSPOSE')
        #for el in self.matrix:
        self.matrix.printTree(indent + 1)

    @addToClass(AST.Uminus)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + "UMINUS")
        self.expression.printTree(indent+1)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + self.id)

    @addToClass(AST.VectorElement)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + "VECTOR ELEMENT")
        self.id.printTree(indent + 1)
        print(TreePrinter.make_indent(indent) + str(self.index))

    @addToClass(AST.MatrixElement)
    def printTree(self, indent=0):
        print(TreePrinter.make_indent(indent) + "MATRIX ELEMENT")
        self.id.printTree(indent + 1)
        print(TreePrinter.make_indent(indent + 1) + str(self.index_x))
        print(TreePrinter.make_indent(indent + 1) + str(self.index_y))

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass


