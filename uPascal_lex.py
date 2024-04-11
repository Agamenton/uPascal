import sys

import ply.lex as lex

keywords = (
    "AND",  # "and"
    "BEGIN",  # "begin"
    "BIN",  # "bin"
    "CHR",  # "chr"
    "DO",  # "do"
    "DOWNTO",  # "downto"
    "ELSE",  # "else"
    "END",  # "end"
    "FOR",  # "for"
    "HEX",  # "hex"
    "IF",  # "if"
    "MOD",  # "mod"
    "NOT",  # "not"
    "OR",  # "or"
    "ORD",  # "ord"
    "READ",  # "read"
    "REPEAT",  # "repeat"
    "SHL",  # "shl"
    "SHR",  # "shr"
    "THEN",  # "then"
    "TO",  # "to"
    "UNTIL",  # "until"
    "WHILE",  # "while"
    "WRITE",  # "write"
    "WRITELN",  # "writeln"
    "XOR",  # "xor"
    "FALSE",  # "false"
    "TRUE",  # "true"
)

tokens = keywords + (
    "RETEZ",  # "'" until next "'"

    "LPAR",  # "("
    "RPAR",  # ")"

    # Operators
    "TIMES",  # "*"
    "DIVIDE",  # "/"
    "BIT_NEG",  # "~"
    "BIT_AND",  # "&"
    # "SHL",  # "<<"
    # "SHR",  # ">>"
    "PLUS",  # "+"
    "MINUS",  # "-"
    "BIT_OR",  # "|"
    "BIT_XOR",  # "!"
    "MENSI",  # "<"
    "VETSI",  # ">"
    "MENSIROVNO",  # "<="
    "VETSIROVNO",  # ">="
    "POROVNANI",  # "="
    "NENIROVNO",  # "<>"
    "PRIRAZENI",  # ":="

    "STREDNIK",  # ";"
    "DVOJTECKA",  # ":"
    "TECKA",  # "."

    "CISLO",  # number
    "PROMENNA",  # variable
)

t_ignore = " \t"


def t_CISLO(t):
    # if starts with $ then it is hex, if starts with % then it is binary, else it is decimal
    r'(\$[0-9a-fA-F]+)|(%[01]+)|([0-9]+)'
    if t.value[0] == '$':
        t.value = int(t.value[1:], 16)
    elif t.value[0] == '%':
        t.value = int(t.value[1:], 2)
    else:
        t.value = int(t.value)
    return t


def t_TRUE(t):
    r"\btrue\b"
    return t

def t_FALSE(t):
    r"\bfalse\b"
    return t

def t_PROMENNA(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in keywords:
        t.type = t.value.upper()
    return t

def t_NOVYRADEK(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_RETEZ(t):
    r"'([^'\n]|\\')*'"
    t.value = t.value[1:-1]  # remove quotes
    return t

t_LPAR = r"\("
t_RPAR = r"\)"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_BIT_NEG = r"~"
t_BIT_AND = r"&"

def t_SHL(t):
    r"<<|shl"
    return t

def t_SHR(t):
    r">>|shr"
    return t

t_PLUS = r"\+"
t_MINUS = r"-"
t_BIT_OR = r"\|"
t_BIT_XOR = r"!"
t_MENSI = r"<"
t_VETSI = r">"
t_MENSIROVNO = r"<="
t_VETSIROVNO = r">="
t_POROVNANI = r"="
t_NENIROVNO = r"<>"
t_PRIRAZENI = r":="
t_STREDNIK = r";"
t_DVOJTECKA = r":"
t_TECKA = r"\."

def t_error(t):
    print("|LexErr| Token: '{}' Radek: {} Sloupec: {}".format(t.value[0], t.lineno, t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos)), file=sys.stderr)

# block comment = { ... }
def t_COMMENT(t):
    r'\{[^}]*\}'
    t.lexer.lineno += t.value.count('\n')
    pass

# line comment = // ...
def t_COMMENT_LINE(t):
    r'//.*'
    pass

uP_lexer = lex.lex()


def tokenize(s):
    uP_lexer.input(s)
    result = []
    while True:
        tok = uP_lexer.token()
        if not tok:
            break
        result.append(tok)
    return result

def test():
    import os
    files_in_dir = os.listdir("Test")
    p = False
    for f in files_in_dir:
        with open("Test/" + f, "r") as file:
            data = file.read()
            toks = tokenize(data)
            print(f"file {f} is OK")
        if not p:
            p = True
            print(file.name)
            for t in toks:
                print(t)


if __name__ == '__main__':
    test()
