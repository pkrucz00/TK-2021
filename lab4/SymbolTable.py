#!/usr/bin/python
class Symbol:
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.var_dict = {}

    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.var_dict[name] = symbol

    #

    def get(self, name):  # get variable symbol or fundef from <name> entry
        try:
            return self.var_dict[name]
        except KeyError:
            if self.parent is None:
                return None
            else:
                return self.getParentScope().get(name)

    #

    def getParentScope(self):
        return self.parent

    #

    def pushScope(self, name):
        return SymbolTable(self, name)

    #

    def popScope(self):
        return self.parent
    #
