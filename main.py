import sys

from uPascal_lex import uP_lexer
from uPascal_par import *
from uzel import *


variables = {}


def interpret(node: Uzel):
    if not node:
        return 0

    typ = node.typ
    if typ == 0:
        interpret(node.prvni())
        interpret(node.druhy())
        interpret(node.treti())
        interpret(node.ctvrty())
        return 0

    elif typ == PRIRAZENI:
        name = node.prvni().promenna()
        val = interpret(node.druhy())
        variables[name] = val
        return val

    elif typ == WRITE:
        if not node.prvni():
            print(end="")
        elif node.druhy():
            length = interpret(node.druhy())
            print(f"{interpret(node.prvni())}"[:length], end="")
        else:
            print(f"{interpret(node.prvni())}", end="")
        return 0

    elif typ == WRITELN:
        if not node.prvni():
            print()
        elif node.druhy():
            length = interpret(node.druhy())
            print(f"{interpret(node.prvni())}"[:length])
        else:
            print(f"{interpret(node.prvni())}")
        return 0

    elif typ == PROMENNA:
        return variables[node.promenna()]

    elif typ == CISLO:
        return node.cislo()

    elif typ == PLUS:
        return interpret(node.prvni()) + interpret(node.druhy())

    elif typ == REPEAT:
        while True:
            interpret(node.prvni())
            if not interpret(node.druhy()):
                break

    elif typ == MINUS:
        return interpret(node.prvni()) - interpret(node.druhy())

    elif typ == MENSI:
        return interpret(node.prvni()) < interpret(node.druhy())

    elif typ == VETSI:
        return interpret(node.prvni()) > interpret(node.druhy())

    else:
        raise TypeError(f"Unknown typ: {typ}")


if __name__ == "__main__":
    # test_file = sys.argv[1]
    test_file = "Test/test1.up"

    with open(test_file, "r") as f:
        code = f.read()

    AST = parser.parse(code, lexer=uP_lexer)
    print(AST)
    try:
        interpret(AST)
    except Exception as e:
        print(e, file=sys.stderr)
