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

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.var_dict[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        return self.var_dict.get(name, default=self.__get_default_value())

    def __get_default_value(self):
        return self.getParentScope().get(name) if self.parent is not None else None

    def getParentScope(self):
        return self.parent

    #

    def pushScope(self, name):
        return SymbolTable(self, name)

    #

    def popScope(self):
        return self.parent
    #
