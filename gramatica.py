

import ply.yacc as yacc
import ply.lex as lex
tokens = (
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ID',
)

# TOKENS

t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS = r'\+'  # se coloca "\" para que no lo tome como 1 ó mas
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'

# ER PARA VALIDAR ENTRE IDENTIFICADORES Y PALABRAS RESERVADAS


def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    return t


# caracteres ignorados
t_ignore = "\t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Ilegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# construyendo analizador lexico
lexer = lex.lex()

# Asociacion de operadores y presedencia
precedence = (
    # HACIA LA IZQUIERDA ASOCIA 4+5+8-> DE ESTA MANERA: (4+5)=9+8 asocia el primer mas con lo de la izquierda suc
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
)


class Recoleccion():
    def __init__(self, ope, opI, opD):
        self.ope = ope
        self.opI = opI
        self.opD = opD

########################################
# definicion de la gramatica


def p_S(t):
    ' s	: e'
    t[0] = t[1]
    print(t[0])
def p_E(t):
    ''' e	: e MAS t 
            | e MENOS t '''

    if t[2] == '+':
        t[0] = Recoleccion('+',t[1], t[3])
    elif t[2] == '-':
        t[0] = Recoleccion('-',t[1], t[3])

def p_ef(t):
    'e : t'
    t[0] = t[1]
 
def p_T(t):
    ''' t	: t POR f 
            | t DIVIDIDO f '''
    if t[2] == '*':
        t[0] = Recoleccion( '*', t[1], t[3])
    elif t[2] == '/':
        t[0] = Recoleccion( '/',t[1], t[3])
        
def p_Tf(t):
    't : f'
    t[0] = t[1]


def p_F_ID(t):
    ' f	: ID '
    t[0] = t[1]

def p_F_PAR(t):
    ' f	: PARIZQ e PARDER '
    t[0] = t[2]


def p_error(t):
    print("Error Sintáctico en '%s'" % t.value)


parser = yacc.yacc()

def sintactico(entrada):
    return parser.parse(entrada)
