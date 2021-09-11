
#REALIZANDO TRADUCCION DESDE EL SINTACTICO

import ply.yacc as yacc
import ply.lex as lex

count = 0
countEtiq=0
lerrores=[]
reservadas={
    'or' : 'OR',
    'and' : 'AND',
    'not' : 'NOT'
}

tokens = [
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ID',
    'ENTERO',
    'DECIMAL',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',
    'IGUAL',
    'DIFERENTE',
    'RTRUE',
    'RFALSE',
]+ list(reservadas.values())

# TOKENS

t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS = r'\+'  # se coloca "\" para que no lo tome como 1 ó mas
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_AND = r'and'
t_OR = r'or'
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_RTRUE = r'true'
t_RFALSE =r'false'


# ER PARA VALIDAR ENTRE IDENTIFICADORES Y PALABRAS RESERVADAS


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
# caracteres ignorados
t_ignore = " \t\r"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Ilegal character '%s'" % t.value[0])
    lerrores.append("Ilegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# construyendo analizador lexico
lexer = lex.lex()

# Asociacion de operadores y presedencia
precedence = (
    # HACIA LA IZQUIERDA ASOCIA 4+5+8-> DE ESTA MANERA: (4+5)=9+8 asocia el primer mas con lo de la izquierda suc
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL','DIFERENTE'),
    ('nonassoc','MAYOR','MENOR' ),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'UMENOS'),
    ('right', 'NOT'),
    ('left','PARIZQ','PARDER'),
)


def new_temp():
    global count
    count = count +1
    etiqueta = 't'+str(count)
    return etiqueta

def new_Etiqueta():
    global countEtiq
    countEtiq = countEtiq+1
    etiquetaa='L'+str(countEtiq)
    return etiquetaa
        

class Informacion():
    def __init__(self,id,tmp,c3d,lv,lf):
        self.id=id
        self.tmp=tmp
        self.c3d=c3d
        self.lv = lv
        self.lf = lf
        
########################################
# definicion de la gramatica

def p_S(t):
    ' s	: p'
    t[0] = t[1]
    print(str(t[0].c3d))
    print("etiquetas verdad: "+str(t[1].lv))
    print("etiquetas falsas: "+str(t[1].lf))
    

def p_p_OR_l(t):
    'p  :   p OR l'
    lv=str(t[1].lv)+ ' , '+str(t[3].lv)
    lf=str(t[3].lf)
    c3d=str(t[1].c3d)+t[1].lf+" : \n"+str(t[3].c3d)
    t[0]=Informacion("","",c3d,lv,lf)

def p_p_l(t):
    'p  : l'
    t[0] = t[1]
    
def p_l_AND_K(t):
    'l  :   l AND n'
    lv=str(t[3].lv)
    lf=str(t[1].lf)+' , '+str(t[3].lf)
    c3d=str(t[1].c3d)+t[1].lv+" : \n"+str(t[3].c3d)
    t[0]=Informacion("","",c3d,lv,lf)

def p_l_k(t):
    'l  : n'
    t[0]=t[1]
    
def p_r_NOT(t):
    'n  :   NOT k'
    lv=str(t[2].lf)
    lf=str(t[2].lv)
    c3d=str(t[2].c3d)
    t[0]=Informacion("","",c3d,lv,lf) 
    
def p_r_NOT1(t):
    'n  :   k'
    t[0]=t[1]
    
def p_k_ma(t):
    'k  : e MAYOR e'
    lv = new_Etiqueta()
    lf = new_Etiqueta()
    c3d=str(t[1].c3d)+str(t[3].c3d)+'if '+str(t[1].tmp)+str(t[1].id)+' > '+str(t[3].tmp)+str(t[3].id)+' goto '+lv+'\r\n'+'goto '+lf+'\r\n'
    t[0]=Informacion("","",c3d,lv,lf)
    #print(str(t[0].c3d),str(t[0].tmp),str(t[0].lv),str(t[0].lf))
def p_k_me(t):
    'k  : e MENOR e'
    lv = new_Etiqueta()
    lf = new_Etiqueta()
    c3d=str(t[1].c3d)+str(t[3].c3d)+'if '+str(t[1].tmp)+str(t[1].id)+' < '+str(t[3].tmp)+str(t[3].id)+' goto '+lv+'\r\n'+'goto '+lf+'\r\n'
    t[0]=Informacion("","",c3d,lv,lf)

def p_k_maigual(t):
    'k  : e MAYORIGUAL e'
    lv = new_Etiqueta()
    lf = new_Etiqueta()
    c3d=str(t[1].c3d)+str(t[3].c3d)+'if '+str(t[1].tmp)+str(t[1].id)+' >= '+str(t[3].tmp)+str(t[3].id)+' goto '+lv+'\r\n'+'goto '+lf+'\r\n'
    t[0]=Informacion("","",c3d,lv,lf)
    #print(str(t[0].c3d),str(t[0].tmp),str(t[0].lv),str(t[0].lf))
def p_k_meigual(t):
    'k  : e MENORIGUAL e'
    lv = new_Etiqueta()
    lf = new_Etiqueta()
    c3d=str(t[1].c3d)+str(t[3].c3d)+'if '+str(t[1].tmp)+str(t[1].id)+' <= '+str(t[3].tmp)+str(t[3].id)+' goto '+lv+'\r\n'+'goto '+lf+'\r\n'
    t[0]=Informacion("","",c3d,lv,lf)

def p_k_ig(t):
    'k  : e IGUAL e'
    lv = new_Etiqueta()
    lf = new_Etiqueta()
    c3d=str(t[1].c3d)+str(t[3].c3d)+'if '+str(t[1].tmp)+str(t[1].id)+' == '+str(t[3].tmp)+str(t[3].id)+' goto '+lv+'\r\n'+'goto '+lf+'\r\n'
    t[0]=Informacion("","",c3d,lv,lf)

def p_k_dif(t):
    'k  : e DIFERENTE e'
    lv = new_Etiqueta()
    lf = new_Etiqueta()
    c3d=str(t[1].c3d)+str(t[3].c3d)+'if '+str(t[1].tmp)+str(t[1].id)+' != '+str(t[3].tmp)+str(t[3].id)+' goto '+lv+'\r\n'+'goto '+lf+'\r\n'
    t[0]=Informacion("","",c3d,lv,lf)



def p_k_ee(t):
    'k  : e'    
    t[0]=t[1]


def p_E(t):
    ''' e	: e MAS e 
            | e MENOS e
            | e POR e
            | e DIVIDIDO e
            '''

    if t[2] == '+':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].id)+str(t[1].tmp)+"+"+str(t[3].id)+str(t[3].tmp)+"\n"#id, solo sirve en la primera pasada
        t[0] = Informacion("",str(Etemp),str(Ec3d),"","")

    elif t[2] == '-':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].id)+str(t[1].tmp)+"-"+str(t[3].id)+str(t[3].tmp)+"\n"
        t[0] = Informacion("",str(Etemp),str(Ec3d),"","")
    elif t[2] == '*':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].id)+str(t[1].tmp)+"*"+str(t[3].id)+str(t[3].tmp)+"\n"
        t[0] = Informacion("",str(Etemp),str(Ec3d),"","")
    
    elif t[2] == '/':
        Etemp = new_temp()
        Ec3d = str(t[1].c3d)+str(t[3].c3d)+str(Etemp)+"="+str(t[1].id)+str(t[1].tmp)+"/"+str(t[3].id)+str(t[3].tmp)+"\n"
        t[0] = Informacion("",str(Etemp),str(Ec3d),"","")
 
def p_e_min(t):
    'e     :   MENOS e %prec UMENOS ' 
    Etemp = new_temp() 
    Ec3d = str(Etemp)+' = 0 -'+str(t[0].id)
    t[0] = Informacion("",str(Etemp),Ec3d,"","") #al ser un numero negativo debe de genera un temporal y c3d -> tn=0-tn



def p_e_ID(t):
    ''' e	: ID 
            | ENTERO
            | DECIMAL
            '''
      
    t[0] = Informacion(str(t[1]),"","","","")#id,tmp,c3d,lv,lf #aqui solo se guardan los numeros o letras que reconozca de la entrada   

def p_e_PAR(t):
    ' e	: PARIZQ p PARDER '
    t[0] = t[2]


def p_error(t):
    print("Error Sintáctico en '%s'" % t.value)
    lerrores.append("Error Sintáctico en '%s'" % t.value)


parser = yacc.yacc()

#el contenido de este archivo es la expresion que usamos el ultimo dia en el periodo de clase.

def analisis(entrada):
    global lerrores
    lerrores=[]
    global count
    count=0
    global countEtiq
    countEtiq=0
    cad=parser.parse(entrada)
    errores=""
    res3d=""
    for err in lerrores:
        errores+=str(err)+"\n"
    
    if isinstance(cad,Informacion):
        res3d+=errores+"\n"
        res3d+=str(cad.c3d)+"\n"
        res3d+="ETIQUETAS VERDADERAS: "+str(cad.lv)+"\n"
        res3d+="ETIQUETAS FALSAS: "    +str(cad.lf)+"\n"
    print(res3d)
    return res3d