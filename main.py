import sys

from uPascal_lex import uP_lexer
from uPascal_par import *
from uzel import *


variables = {}


def write(node, ln=False):
    end = "\n" if ln else ""
    if not node.prvni():
        print(end=end)
    elif node.druhy():
        spaces = interpret(node.druhy())
        val = interpret(node.prvni())
        length = len(str(val))
        if length < spaces:
            val = f"{''.join([' ' for _ in range(spaces - length)])}{val}"
        print(f"{val}", end=end)

    else:
        print(f"{interpret(node.prvni())}", end=end)
    return 0


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

    # ---------------------------------
    # ------- Builtin functions -------
    elif typ == WRITE:
        write(node)
        return 0

    elif typ == WRITELN:
        write(node, ln=True)
        return 0

    elif typ == READ:
        name = node.prvni().promenna()

        user_input = input()
        if user_input.isdigit():
            user_input = int(user_input)
        else:  # if user entered string return ASCII value of first character
            user_input = ord(user_input[0])

        variables[name] = user_input
        return 0

    elif typ == BIN:
        return bin(interpret(node.prvni()))[2:]     # skip first 2 chars (0b)

    elif typ == HEX:
        return hex(interpret(node.prvni()))[2:]     # skip first 2 chars (0x)

    elif typ == CHR:
        return chr(interpret(node.prvni()))

    elif typ == ORD:
        return ord(interpret(node.prvni()))

    # ---------------------------------
    # ------------ Types --------------
    elif typ == PROMENNA:
        return variables[node.promenna()]

    elif typ == CISLO:
        return node.cislo()

    elif typ == RETEZ:
        return node.retez()

    # ---------------------------------
    # ---------- Operators ------------
    elif typ == PLUS:
        return interpret(node.prvni()) + interpret(node.druhy())

    elif typ == MINUS:
        if not node.druhy():
            return -interpret(node.prvni())
        return interpret(node.prvni()) - interpret(node.druhy())

    elif typ == TIMES:
        return interpret(node.prvni()) * interpret(node.druhy())

    elif typ == DIVIDE:
        return interpret(node.prvni()) // interpret(node.druhy())

    elif typ == MOD:
        return interpret(node.prvni()) % interpret(node.druhy())

    elif typ == BIT_AND:
        return interpret(node.prvni()) & interpret(node.druhy())

    elif typ == BIT_OR:
        return interpret(node.prvni()) | interpret(node.druhy())

    elif typ == BIT_XOR:
        return interpret(node.prvni()) ^ interpret(node.druhy())

    elif typ == BIT_NEG:
        return ~interpret(node.prvni())

    elif typ == SHR:
        return interpret(node.prvni()) >> interpret(node.druhy())

    elif typ == SHL:
        return interpret(node.prvni()) << interpret(node.druhy())

    elif typ == NENIROVNO:
        return interpret(node.prvni()) != interpret(node.druhy())

    elif typ == POROVNANI:
        return interpret(node.prvni()) == interpret(node.druhy())

    elif typ == MENSI:
        return interpret(node.prvni()) < interpret(node.druhy())

    elif typ == VETSI:
        return interpret(node.prvni()) > interpret(node.druhy())

    elif typ == VETSIROVNO:
        return interpret(node.prvni()) >= interpret(node.druhy())

    elif typ == MENSIROVNO:
        return interpret(node.prvni()) <= interpret(node.druhy())

    elif typ == AND:
        return interpret(node.prvni()) and interpret(node.druhy())

    elif typ == OR:
        return interpret(node.prvni()) or interpret(node.druhy())

    elif typ == NOT:
        return not interpret(node.prvni())

    elif typ == XOR:
        return interpret(node.prvni()) != interpret(node.druhy())

    # ---------------------------------
    # ---------- Statements ------------
    elif typ == BEGIN:
        while interpret(node.prvni()):
            interpret(node.druhy())

    elif typ == IF:
        if interpret(node.prvni()):
            interpret(node.druhy())
        else:
            if node.treti():
                interpret(node.treti())

    elif typ == WHILE:
        while interpret(node.prvni()):
            interpret(node.druhy())

    elif typ == FOR:
        for i in range(interpret(node.druhy()), interpret(node.treti())+1):
            variables[node.prvni().promenna()] = i
            interpret(node.ctvrty())

    elif typ == FORDOWN:
        for i in range(interpret(node.druhy()), interpret(node.treti())-1, -1):
            variables[node.prvni().promenna()] = i
            interpret(node.ctvrty())

    elif typ == REPEAT:
        while True:
            interpret(node.prvni())
            if interpret(node.druhy()):
                break

    else:
        raise TypeError(f"Unknown typ: {typ}")


if __name__ == "__main__":
    test_file = sys.argv[1]

    with open(test_file, "r") as f:
        code = f.read()

    AST = parser.parse(code, lexer=uP_lexer)

    try:
        interpret(AST)
    except Exception as e:
        print(e, file=sys.stderr)
        raise e
