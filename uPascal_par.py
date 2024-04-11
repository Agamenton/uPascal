import sys

from uPascal_lex import uP_lexer, tokens, tokenize
import ply.yacc as yacc
from uzel import *

precedence = (
    ("left", "POROVNANI", "NENIROVNO", "MENSI", "VETSI", "MENSIROVNO", "VETSIROVNO"),
    ("left", "PLUS", "MINUS", "OR", "XOR", "BIT_OR", "BIT_XOR"),
    ("left", "TIMES", "DIVIDE", "MOD", "AND", "BIT_AND", "SHL", "SHR"),
    ("right", "NOT", "BIT_NEG"),
)


# Grammar rules
def p_program(p):
    """program : BEGIN program1 TECKA"""
    p[0] = p[2]


def p_program1(p):
    '''program1 : prikaz program2'''
    p[0] = GenUzel(0, p[1], p[2]) if p[2] else p[1]


def p_program2(p):
    '''program2 : STREDNIK program3
                | END'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = 0


def p_program3(p):
    '''program3 : END
                | prikaz program2'''
    if len(p) == 2:
        p[0] = 0
    else:
        p[0] = GenUzel(0, p[1], p[2]) if p[2] else p[1]


def p_prikaz_assign(p):
    '''prikaz : promenna PRIRAZENI vyraz'''
    p[0] = GenUzel(PRIRAZENI, p[1], p[3])


def p_prikaz_begin(p):
    '''prikaz : BEGIN program1'''
    p[0] = p[2]


def p_prikaz_if(p):
    '''prikaz : IF vyraz THEN prikaz
              | IF vyraz THEN prikaz ELSE prikaz'''
    if len(p) == 5:
        p[0] = GenUzel(IF, p[2], p[4])
    else:
        p[0] = GenUzel(IF, p[2], p[4], p[6])


def p_prikaz_for(p):
    '''prikaz : FOR promenna PRIRAZENI vyraz for vyraz DO prikaz'''
    p[0] = GenUzel(p[5], p[2], p[4], p[6], p[8])


def p_for(p):
    '''for : TO
           | DOWNTO'''
    p[0] = FOR if p[1] == 'to' else FORDOWN


def p_prikaz_while(p):
    '''prikaz : WHILE vyraz DO prikaz'''
    p[0] = GenUzel(WHILE, p[2], p[4])


def p_prikaz_repeat(p):
    '''prikaz : REPEAT prikazy UNTIL vyraz'''
    p[0] = GenUzel(REPEAT, p[2], p[4])


def p_prikaz_error(p):
    '''prikaz : error STREDNIK '''
    p[0] = None


def p_prikazy(p):
    '''prikazy : prikaz STREDNIK prikazy1'''
    if p[3]:
        p[0] = GenUzel(0, p[1], p[3])
    else:
        p[0] = p[1]


def p_prikazy1(p):
    '''prikazy1 : prikaz STREDNIK prikazy1
                |'''
    if len(p) == 4:
        p[0] = p[3]
        if p[1]:
            if p[3]:
                p[0] = GenUzel(0, p[1], p[3])
            else:
                p[0] = p[1]
    else:
        p[0] = None


def p_prikaz_write(p):
    '''prikaz : WRITELN
              | write LPAR retez RPAR '''
    if p[1] == 'writeln':
        p[0] = GenUzel(WRITELN)
    else:
        p[0] = GenUzel(p[1], p[3])


def p_write(p):
    '''write : WRITE
             | WRITELN'''
    p[0] = WRITE if p[1] == 'write' else WRITELN


def p_retez(p):
    '''retez : RETEZ'''
    p[0] = GenRetez(p[1])


def p_prikaz_write_expression(p):
    '''prikaz : write LPAR write2 write3 RPAR '''
    p[0] = GenUzel(p[1], p[3], p[4])


def p_write2(p):
    '''write2 : vyraz
              | CHR LPAR vyraz RPAR
              | HEX LPAR vyraz RPAR
              | BIN LPAR vyraz RPAR '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == 'chr':
            p[0] = GenUzel(CHR, p[3])
        elif p[1] == 'hex':
            p[0] = GenUzel(HEX, p[3])
        else:
            p[0] = GenUzel(BIN, p[3])


def p_write3(p):
    '''write3 : DVOJTECKA cislo
              |'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_prikaz_read(p):
    '''prikaz : READ LPAR promenna RPAR '''
    user_input = input()
    if user_input.isdigit():
        user_input = int(user_input)
    else:   # if user entered string return ASCII value of first character
        user_input = ord(user_input[0])
    p[3] = user_input
    p[0] = GenUzel(READ, p[3])


def p_vyraz_unary(p):
    '''vyraz : NOT vyraz
             | BIT_NEG vyraz
             | PLUS vyraz
             | MINUS vyraz
             | LPAR vyraz RPAR '''
    if p[1] == "!":
        if Konst(p[2]):
            p[2].z["Cislo"] = not p[2].z["Cislo"]
            p[0] = p[2]
        else:
            p[0] = GenUzel(NOT, p[2])
    elif p[1] == "~":
        if Konst(p[2]):
            p[2].z["Cislo"] = ~p[2].z["Cislo"]
            p[0] = p[2]
        else:
            p[0] = GenUzel(BIT_NEG, p[2])
    elif p[1] == "+":
        p[0] = p[2]
    elif p[1] == "-":
        if Konst(p[2]):
            p[2].z["Cislo"] = -p[2].z["Cislo"]
            p[0] = p[2]
        else:
            p[0] = GenUzel(MINUS, p[2])
    else:
        p[0] = p[2]

def p_vyraz_boolean(p):
    '''vyraz : TRUE
             | FALSE'''
    p[0] = GenCislo(0xFFFFFFFF if p[1] == 'true' else 0) # used numbers because bools can be handled as numbers anyway

def p_vyraz_binary(p):
    '''vyraz : vyraz TIMES vyraz
             | vyraz DIVIDE vyraz
             | vyraz MOD vyraz
             | vyraz AND vyraz
             | vyraz BIT_AND vyraz
             | vyraz SHL vyraz
             | vyraz SHR vyraz
             | vyraz PLUS vyraz
             | vyraz MINUS vyraz
             | vyraz OR vyraz
             | vyraz XOR vyraz
             | vyraz BIT_OR vyraz
             | vyraz BIT_XOR vyraz
             | vyraz MENSI vyraz
             | vyraz VETSI vyraz
             | vyraz MENSIROVNO vyraz
             | vyraz VETSIROVNO vyraz
             | vyraz POROVNANI vyraz
             | vyraz NENIROVNO vyraz '''
    if p[2] == "*":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] *= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(TIMES, p[1], p[3])
    elif p[2] == "/":
        if Konst2(p[1], p[3]):
            if p[3].z["Cislo"] != 0:
                p[1].z["Cislo"] /= p[3].z["Cislo"]
            else:
                raise ValueError("Deleni nulou")
            p[0] = p[1]
        else:
            p[0] = GenUzel(DIVIDE, p[1], p[3])
    elif p[2] == 'mod':
        if Konst2(p[1], p[3]):
            if p[3].z["Cislo"] != 0:
                p[1].z["Cislo"] %= p[3].z["Cislo"]
            else:
                raise ValueError("Deleni nulou")
            p[0] = p[1]
        else:
            p[0] = GenUzel(MOD, p[1], p[3])
    elif p[2] == 'and':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] and p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(AND, p[1], p[3])
    elif p[2] == "&":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] &= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(BIT_AND, p[1], p[3])
    elif p[2] == 'shl':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] <<= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(SHL, p[1], p[3])
    elif p[2] == 'shr':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] >>= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(SHR, p[1], p[3])
    elif p[2] == "+":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] += p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(PLUS, p[1], p[3])
    elif p[2] == "-":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] -= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(MINUS, p[1], p[3])
    elif p[2] == 'or':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] or p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(OR, p[1], p[3])
    elif p[2] == 'xor':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = (p[1].z["Cislo"] and not p[3].z["Cislo"]) or (not p[1].z["Cislo"] and p[3].z["Cislo"])
            p[0] = p[1]
        else:
            p[0] = GenUzel(XOR, p[1], p[3])
    elif p[2] == "|":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] |= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(BIT_OR, p[1], p[3])
    elif p[2] == "!":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] ^= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(BIT_XOR, p[1], p[3])
    elif p[2] == "<":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] < p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(MENSI, p[1], p[3])
    elif p[2] == ">":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] > p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(VETSI, p[1], p[3])
    elif p[2] == '<=':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] <= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(MENSIROVNO, p[1], p[3])
    elif p[2] == '>=':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] >= p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(VETSIROVNO, p[1], p[3])
    elif p[2] == "=":
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] == p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(POROVNANI, p[1], p[3])
    elif p[2] == '!=':
        if Konst2(p[1], p[3]):
            p[1].z["Cislo"] = p[1].z["Cislo"] != p[3].z["Cislo"]
            p[0] = p[1]
        else:
            p[0] = GenUzel(NENIROVNO, p[1], p[3])

def p_vyraz_ord(p):
    '''vyraz : ORD LPAR retez RPAR '''
    p[0] = GenUzel(ORD, p[3])


def p_vyraz_promenna(p):
    '''vyraz : promenna'''
    p[0] = p[1]


def p_vyraz_cislo(p):
    '''vyraz : cislo'''
    p[0] = p[1]


def p_cislo(p):
    '''cislo : CISLO'''
    p[0] = GenCislo(p[1])


def p_promenna(p):
    '''promenna : PROMENNA'''
    p[0] = GenPromen(p[1])


# Error rule for syntax errors
def p_error(p):
    print("|SyntErr| Token: '{}' Radek: {} Sloupec: {}".format(p.value, p.lineno, p.lexpos - p.lexer.lexdata.rfind('\n', 0, p.lexpos)), file=sys.stderr)


parser = yacc.yacc()

if __name__ == '__main__':
    test_file = "Test/test1.up"
    with open(test_file, 'r') as f:
        data = f.read()
        result = parser.parse(data, lexer=uP_lexer)
    print(result)
    # import os
    #
    # files_in_dir = os.listdir("Test")
    # p = False
    # for f in files_in_dir:
    #     with open("Test/" + f, "r") as file:
    #         data = file.read()
    #         uP_lexer.lineno = 1
    #         result = parser.parse(data, lexer=uP_lexer)
    #         print(f"file {f} is OK")
