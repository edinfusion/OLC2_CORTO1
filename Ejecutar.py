import gramatica as g

count = 0


def newTemp():
    'genera etiquetas t0,t1,t2..tn'
    global count
    count += 1
    etiqueta = 't'+str(count)
    return etiqueta


def RecorrerArbol(raiz):
   # print(raiz)
    if isinstance(raiz, str): #si es un string devolver a izTmp
        return (raiz, "")
    else:
        izTmp, izC3D = RecorrerArbol(raiz.opI)
        derTmp, derC3D = RecorrerArbol(raiz.opD)
        ope = raiz.ope
        etiqueta = newTemp()
        return (etiqueta, izC3D + derC3D + "\n"+etiqueta+" = "+izTmp + " "+ope+" "+derTmp)

ast = g.sintactico("a+b+c")
tmps, c3d = RecorrerArbol(ast)
print(c3d)
 
count =0
ast = g.sintactico("a-b*(c+d)")
tmps, c3d = RecorrerArbol(ast)
print(c3d)

count=0
ast = g.sintactico("a+b*c*d*f+(a-b)/(a/f)")
tmps, c3d = RecorrerArbol(ast)
print(c3d)

count=0
ast = g.sintactico("f+g+c*(a+b)")
tmps, c3d = RecorrerArbol(ast)
print(c3d)
