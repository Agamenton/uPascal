# typedef struct uzel_s {
#
#     int Typ;
#
#     union {
#         struct { struct uzel_s *prvni,*druhy,*treti,*ctvrty; } z;
#         int Cislo;
#         const char *Retez;
#         int *Adresa;
#     } z;
#
# } Uzel;


# Types:
CISLO = 'CISLO'
RETEZ = 'RETEZ'
PROMENNA = 'PROMENNA'
BEGIN = 'begin'
BIN = 'BIN'
DO = 'DO'
ELSE = 'ELSE'
END = 'END'
FOR = 'FOR'
FORDOWN = 'FORDOWN'
HEX = 'HEX'
CHR = 'CHR'
IF = 'IF'
ORD = 'ORD'
READ = 'READ'
REPEAT = 'REPEAT'
THEN = 'THEN'
TO = 'TO'
UNTIL = 'UNTIL'
WHILE = 'WHILE'
WRITE = 'WRITE'
WRITELN = 'WRITELN'
PRIRAZENI = 'PRIRAZENI'
VETSIROVNO = 'VETSIROVNO'
MENSIROVNO = 'MENSIROVNO'
NENIROVNO = 'NENIROVNO'
XOR = 'XOR'
OR = 'OR'
SHR = 'SHR'
SHL = 'SHL'
AND = 'AND'
MOD = 'MOD'
NOT = 'NOT'
BIT_NOT = 'BIT_NOT'
LPAR = 'LPAREN'
RPAR = 'RPAREN'
TIMES = 'TIMES'
DIVIDE = 'DIVIDE'
SEMICOLON = 'SEMICOLON'
COMMA = 'COMMA'
COLON = 'COLON'
DOT = 'DOT'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
COMMENT = 'COMMENT'
PLUS = 'PLUS'
MINUS = 'MINUS'
BIT_XOR = 'BIT_XOR'
BIT_OR = 'BIT_OR'
BIT_AND = 'BIT_AND'
MENSI = "MENSI"
VETSI = "VETSI"
POROVNANI = "POROVNANI"
BIT_NEG = "BIT_NEG"


class Uzel:
    def __init__(self, typ, z=None):
        self.typ = typ
        self.z = z if z is not None else {}

    def __str__(self):
        return f'Uzel(typ={self.typ} z={str(self.z)})\n'

    def __repr__(self):
        return self.__str__()


def GenUzel(typ, z1=None, z2=None, z3=None, z4=None):
    return Uzel(typ, {'prvni': z1, 'druhy': z2, 'treti': z3, 'ctvrty': z4})


def GenCislo(cislo):
    return Uzel('CISLO', {'Cislo': cislo})


def GenPromen(promen):
    return Uzel('PROMENNA', {'Adresa': promen})


def GenRetez(retez):
    return Uzel('RETEZ', {'Retez': retez})


def Konst(u: Uzel) -> bool:
    return u and u.typ == 'CISLO'


def Konst2(u1: Uzel, u2: Uzel) -> bool:
    return Konst(u1) and Konst(u2)


Koren = None


def get_Koren():
    return Koren


def set_Koren(koren):
    global Koren
    Koren = koren
