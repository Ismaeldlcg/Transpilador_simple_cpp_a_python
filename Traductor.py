import ply.lex as lex
import ply.yacc as yacc

#Analizador lexico

reserved = {
	'include' : 'INCLUDE',
	'iostream' : 'IOSTREAM',
	'using' : 'USING',
	'namespace' : 'NAMESPACE',
	'std' : 'STD',
	'int' : 'INT',
	'float' : 'FLOAT',
	'return' : 'RETURN',
	'else' : 'ELSE',
	'if' : 'IF',
	'cout' : 'COUT',
	'endl' : 'ENDL',
    'while' : 'WHILE',
    'do' : 'DO',
    'break' : 'BREAK',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'cin' : 'CIN',
}


tokens = ['ID', 'COMA', 'PARENA', 'PARENC', 'OPBIN', 'OPUNA', 'IGUALES', 'NUM', 'EXPBOOL', 
		  'COMENT', 'STRING', 'DOBLER', 'PUNTOYCOMA','MICHI','LTGT', 'CORCHETES', 'LLAVES', 
		  'PARENTESIS', 'NUMERO', 'OPERACIONES',
		  ]

tokens = tokens + list(reserved.values())

m_tabs = 0
m_result = ""
m_totLineas = 1
m_reporte = ""

t_PUNTOYCOMA = r';'
t_MICHI = r'\#'
t_ignore = " \t"

def t_PARENTESIS(t):
	r'\(|\)'
	return t

def t_LLAVES(t):
	r'\{|\}'
	return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_DOBLER(t):
	r'\<<|\<|\>'
	return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMA(t):
	r','
	return t

def t_OPERACIONES(t):
	r'\+|\-|\*|\/'
	return t

def t_IGUALES(t):
	r'=|\+=|-=|\==|/='
	return t

def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_COMENT(t):
	r'\$'
	return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_newline(t):
	r'\n'
	global m_totLineas
	m_totLineas += 1

def t_error (t):
    print ("Error lexico")
    t.lexer.skip(1)

lex.lex()

#Analizador sintactico

# Metodo auxiliar que se encarga de hacer la identacion de cada linea en python
def add_tabs(b):
	global m_tabs
	nivel = ''
	if(b == False):
		nivel = "\n" # para hacer el cambio de linea despues de la instruccion
	tmp = m_tabs
	while tmp > 0:	# agrega tantos tabs como lo inque m_tabs
		nivel += "\t"
		tmp = tmp -1
	return nivel

def p_root(p):
	'''root : inicio'''
	p[0] = str(p[1])
	global m_result
	m_result += str(p[0])

def p_inicio(p):
	'''inicio : instruccion inicio'''
	p[0] = str(p[1]) + str(p[2])

def p_inicio2(p):
	'''inicio : epsilon'''
	p[0] = str(p[1])

def p_epsilon(p):
	'''epsilon : '''
	p[0] = ''

def p_opestring(p):
	'''opestring : STRING '''
	p[0] = str(p[1])
	
def p_programa(p):
    'programa : MICHI INCLUDE DOBLER IOSTREAM DOBLER USING NAMESPACE STD PUNTOYCOMA bloque'
    p[0] = add_tabs(False) + str(p[10])

def p_bloque(p):
	'bloque : basico ID PARENTESIS PARENTESIS LLAVES decls mostrarvarios condicion RETURN NUMERO PUNTOYCOMA LLAVES'
	p[0] = add_tabs(False) + str(p[6]) + str(p[7]) + str(p[8])
	
def p_mostrarvarios(p):
	''' mostrarvarios : mostrarvarios mostrar
                      | mostrarvarios mostrardatos
	                  | epsilon '''
	if len(p) == 3:
		p[0] = str(p[1]) + str(p[2])
	else:
		p[0] = ''

def p_mostrardatos(p):
	' mostrardatos : COUT DOBLER ID DOBLER ENDL PUNTOYCOMA '
	p[0] = add_tabs(False) + 'print(' + str(p[3]) + ')'

def p_mostrar(p):
	'mostrar : COUT DOBLER opestring DOBLER ENDL PUNTOYCOMA '
	p[0] = add_tabs(False) + 'print(' + str(p[3]) + ')'
	
def p_condicionif(p):
	'''condicionif : IF PARENTESIS ID DOBLER NUMERO PARENTESIS LLAVES decls mostrarvarios LLAVES'''
	p[0] = add_tabs(False) + 'if ' + ' ' + str(p[3])+ ' ' + str(p[4])+ ' ' + str(p[5]) + ':' + '...' + str(p[9])

def p_condicionelse(p):
	'''condicionelse : ELSE LLAVES decls mostrarvarios LLAVES '''
	p[0] = add_tabs(False) +'else:' + '\t' + str(p[4])

def p_condicion(p):
	'''condicion : condicionif
	             | condicionelse '''
	p[0] = str(p[1])

def p_decls(p):
    '''
    decls : decls decljuntos
          | epsilon

    '''
    if len(p) == 3:
        p[0] = str(p[1]) + '\n' + str(p[2])
    else:
         p[0] = ''
		 
def p_decljuntos(p):
	'''decljuntos : decl
	              | decl2 
				  | operaciones '''
	p[0] = str(p[1])

def p_decl2(p):
	'''
    decl2 : tipo ID PUNTOYCOMA
	
    '''
	p[0] = str(p[2])

def p_decl(p):
	'''
    decl : tipo ID IGUALES NUMERO PUNTOYCOMA
	
    '''
	p[0] = str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4])

def p_operaciones(p):
    ' operaciones : tipo ID IGUALES operacion PUNTOYCOMA '
    p[0] = str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4])

def p_operacion(p):
	' operacion : ID OPERACIONES ID '
	p[0] = str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3])

def p_tipo(p):
	'''
    tipo : basico

    '''
	p[0] = str(p[1])

def p_basico(p):
	'''
    basico : INT
           | FLOAT
	'''
	p[0] = str(p[1])

def p_instruccion(p):
	''' instruccion : programa '''
	global m_tabs
	p[0] = str(p[1])

def p_error(p):
	global m_totLineas
	global m_reporte
	if p:
		m_reporte +="Error de sintaxis en " + str(p.value) + ". En la linea " + str(m_totLineas)+'\n'
		print(m_reporte)
	else:
		m_reporte += "Error en "+str(m_totLineas)+'\n'
		print(m_reporte)
	exit()
	m_reporte = ""

yacc.yacc()

sfname = ""
sfname = str(input('Ingrese el nombre del archivo que desea transpilar a python> '))
sourceFile = open(sfname+".cpp", 'r')
cpp = ""
for line in sourceFile:
	cpp += str(line)
yacc.parse(cpp)
sfname = str(input('Ingrese el nombre con el que quiere guardar el archivo> '))
file = open(sfname+".py", 'w')
file.write(m_result)
file.close()
sourceFile.close()