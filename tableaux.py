#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
conectivosbinarios = ['Y','O','>','<->']
negacion = ['-']
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
    letrasProposicionales=[chr(x) for x in range(256, 600)]
    conectivosbinarios = ['Y', 'O', '>', '=']
    negacion = ["-"]
    Pila = []
    for c in A:
        if c in letrasProposicionales:
            Pila.append(Tree(c,None,None))
        elif c in negacion :
            FormulaAux = Tree(c,None,Pila[-1])
            del Pila[-1]
            Pila.append(FormulaAux)
        elif c in conectivosbinarios:
            FormulaAux = Tree(c,Pila[-1],Pila[-2])
            del Pila[-1]
            del Pila[-1]
            Pila.append(FormulaAux)
        else:
            print(u"Hay un problema: el símbolo " + str(c)+ " no se reconoce")
    return Pila[-1]
	# OJO: DEBE INCLUIR SU CÓDIGO DE STRING2TREE EN ESTA PARTE!!!!!

	

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def complemento(l):
	# Esta función devuelve el complemento de un literal
	# Input: l, un literal
	# Output: x, un literal
    if l[0] in negacion:
        a=Tree(l[1],None,None)
    elif l[0] in conectivosbinarios:
        pass
    else:
        a=Tree('-',None,Tree(l,None,None))
    return a
def par_complementario2(l):
    for i in l:
        if (i.label in conectivosbinarios):
            pass
        elif (i.label in negacion):
            if (i.right.label in negacion):
                pass
            else:
                a='-'+i.label.right
                if (complemento(a)in l):
                    return True
        else:
            a=i.label
            if (complemento(a)in l):
                return True
    return False
def es_literal(f):
    # Esta función determina si el árbol f es un literal
    # Input: f, una fórmula como árbol
    # Output: True/False
    if f.label in negacion:
        if (f.right.label in negacion) or (f.right.label in conectivosbinarios):
            return False
        else:
            return True
    elif f.label in conectivosbinarios:
        return False
    else:
        return True

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	
    	for i in l:
        	if es_literal(i)==False:
            		return True
        else:
            	pass
    	return False

def clasificacion(f):
	# clasifica una fórmula como alfa o beta
	# Input: f, una fórmula como árbol
	# Output: string de la clasificación de la formula
   # if f.label  == "=":
    #    return "Alfa5" + "("+f.left+"->"+f.right+")"+"Y"+"("+f.right+"->"+f.left+")"
    if f.label == "Y":
        return "Alfa2" #+  "("+f.left+")"+"Y"+"("+f.right+")"
    elif f.label == "-" and f.right == "O":
        return "Alfa3"#+"("+"-"+f.left+")"+"Y"+"("+"-"+f.right+")"
    elif f.label == "-" and f.right == "->":
        return "Alfa4"#+"("+f.left+")"+"Y"+"("+"-"+f.right+")"
    elif f.label == "-" and f.right == "-":
        return "Alfa1"#+"("+f.right+")"
    elif f.label == ">":
        return "Beta3"# + "("+"-"+f.left+")"+"O"+"("+f.right+")" 
    elif f.label == "O":
        return "Beta2"# + "("+f.left+")"+"O"+"("+f.right+")" 
    elif f.label == "-" and f.right == "Y":
        return "Beta1"# + "("+"-"+f.left+")"+"O"+"("+"-"+f.right+")" 

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
    if clasificacion(f)== "Alfa1":
        derecho = f.right.right
        listaHojas.remove([f]) #elimina la lista f 
        listaHojas.append(derecho)#doble negación
    elif clasificacion(f)== "Alfa2":
        izquierdo = f.left
        derecho = f.right
        listaHojas.remove([f]) #elimina la lista f 
        lista = [izquierdo,derecho]
        listaHojas.append(lista)
    elif clasificacion(f)== "Alfa3":
        izquierdo = Tree("-", None,f.left)
        derecho = Tree("-",None,f.right)
        listaHojas.remove([f]) #elimina la lista f 
        lista = [izquierdo,derecho]
        listaHojas.append(lista)
    elif clasificacion(f)== "Alfa4":
        izquierdo = f.left
        derecho = Tree("-",None,f.right)
        lista = [izquierdo,derecho]
        listaHojas.remove([f]) #elimina la lista f 
        listaHojas.append(lista)
    elif clasificacion(f)== "Beta1":
        izquierdo = Tree("-",None,f.left)
        derechoo = Tree("-",None,f.right)
        listaHojas.remove([f])
        listaHojas.append(izquierdo)
        listaHojas.append(derecho)
    elif clasificacion(f)== "Beta2":
        izquierdo = f.left
        dercho = f.right
        listaHojas.remove([f])
        listaHojas.append(izquierdo)
        listaHojas.append(derecho)
    elif clasificacion(f)== "Beta3":
        izquierdo = Tree("-",None,f.left)
        derecho = f.right
        listaHojas.remove([f])
        listaHojas.append(izquierdo)
        listaHojas.append(derecho)
	global listaHojas

def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
	global listaHojas
	global listaInterpsVerdaderas
    
	A = StringtoTree(f)
	listaHojas = [[A]]
    while len(listaHojas)>0:
        hoja= choice(listaHojas)
        if (no_literales(hoja)==True):
            if (par_complementario(hoja)==True):
                listaHojas.remove(hoja)
            else:
                listaInterpsVerdaderas.append(hoja)
                listaHojas.remove(hoja)
        else:
            clasifica_y_extiende(hoja)

    return listaInterpsVerdaderas
