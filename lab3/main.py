
import sys
import ply.yacc as yacc
import Mparser
from TreePrinter import TreePrinter


if __name__ == '__main__':

    # try:
    #     filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
    #     file = open(filename, "r")
    # except IOError:
    #     print("Cannot open {0} file".format(filename))
    #     sys.exit(0)

    # Mparser = Mparser.Mparser()
    parser = Mparser.parser
    # text = file.read()
    text = "ABC"
    ast = parser.parse(text, lexer=Mparser.scanner)
    ast.printTree()