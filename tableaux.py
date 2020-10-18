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
    if f.label == 'Y':
        return "Alfa2" 
    elif f.label == '-' and f.right.label == 'O':
        return "Alfa3"
    elif f.label == '-' and f.right.label == '>':
        return "Alfa4"
    elif f.label == '-' and f.right.label == '-':
        return "Alfa1"
    elif f.label == '>':
        return "Beta3"
    elif f.label == 'O':
        return "Beta2"
    elif f.label == '-' and f.right.label == 'Y':
        return "Beta1" 
    else:
        return "error en la clasificacion"


def clasifica_y_extiende(f, h):
	global listaHojas
	print("Formula:", Inorder(f))
	print("Hoja:", imprime_hoja(h))
	assert(f in h), "La formula no esta en la lista!"
	clase = clasificacion(f)
	print("Clasificada como:", clase)
	assert(clase != None), "Formula incorrecta " + imprime_hoja(h)
	if clase == 'Alfa1':
		aux = [x for x in h if x != f] + [f.right.right]
		listaHojas.remove(h)
		listaHojas.append(aux)
	elif clase == 'Alfa2':
		aux = [x for x in h if x != f] + [f.right] + [f.left]
		listaHojas.remove(h)
		listaHojas.append(aux)
	elif clase == 'Alfa3':
		aux = [x for x in h if x != f] + [complemento(f.right.left.label)] + [complemento(f.right.right.label)]
		listaHojas.remove(h)
		listaHojas.append(aux)
	elif clase == 'Alfa4':
		aux = [x for x in h if x != f] + [f.right.left] + [complemento(f.right.right.label)]
		listaHojas.remove(h)
		listaHojas.append(aux)
	elif clase == 'Beta1':
		aux = [x for x in h if x != f] + [complemento(f.right.left.label)]
		listaHojas.remove(h)
		listaHojas.append(aux)
		aux2 = [x for x in h if x != f] + [complemento(f.right.right.label)]
		listaHojas.append(aux2)
	elif clase == 'Beta2':
		aux =  [x for x in h if x != f] + [f.right]
		listaHojas.remove(h)
		listaHojas.append(aux)
		aux2 = [x for x in h if x != f]+ [f.left]
		listaHojas.append(aux2)
	elif clase == 'Beta3':
		aux = [x for x in h if x != f ] + [complemento(f.right.left.label)]
		listaHojas.remove(h)
		listaHojas.append(aux)
		aux2 = [x for x in h if x != f]+ [f.left]
		listaHojas.append(aux2)

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
