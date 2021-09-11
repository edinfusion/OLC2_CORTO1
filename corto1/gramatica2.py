
#REALIZANDO TRADUCCION DESDE EL SINTACTICO

import ply.yacc as yacc
import ply.lex as lex

count = 0

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
t_ignore = " \t"


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


def new_temp():
    global count
    count = count +1
    etiqueta = 't'+str(count)
    return etiqueta
        

class Informacion():
    def __init__(self,tmp,c3d):
        self.tmp=tmp
        self.c3d=c3d
        
########################################
# definicion de la gramatica


def p_S(t):
    ' s	: e'
    t[0] = t[1]
    print("TRADUCCION C3D: \n"+str(t[0].c3d))
def p_E(t):
    ''' e	: e MAS t 
            | e MENOS t  '''

    if t[2] == '+':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+ str(Etemp)+"="+str(t[1].tmp)+"+"+str(t[3].tmp+"\n")
        t[0] = Informacion(str(Etemp),str(Ec3d))
    
    elif t[2] == '-':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].tmp)+"-"+str(t[3].tmp+"\n")
        t[0] = Informacion(str(Etemp),str(Ec3d))
        
def p_et(t):
    'e : t'
    t[0] = t[1]
    
def p_T(t):
    ''' t	: t POR f 
            | t DIVIDIDO f  '''

    if t[2] == '*':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].tmp)+"*"+str(t[3].tmp+"\n")
        t[0] = Informacion(str(Etemp),str(Ec3d))
    
    elif t[2] == '/':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].tmp)+"/"+str(t[3].tmp+"\n")
        t[0] = Informacion(str(Etemp),str(Ec3d))
        
def p_tf(t):
    't : f'
    t[0] = t[1]
    

def p_F_ID(t):
    ' f	: ID '
    t[0] = Informacion(str(t[1]),"")
    

def p_F_PAR(t):
    ' f	: PARIZQ e PARDER '
    t[0] = t[2]


def p_error(t):
    print("Error Sintáctico en '%s'" % t.value)


parser = yacc.yacc()

entrada = "a+b+c/d*c"

parser.parse(entrada)
