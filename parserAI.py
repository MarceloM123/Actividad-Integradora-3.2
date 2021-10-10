# <prog> ::= <exp> <prog> | $
# <exp> ::= <atomo> | <lista>
# <atomo> ::= simbolo | <constante>
# <constante> ::= numero | booleano | string
# <lista> ::= ( <elementos> )
# <elementos> ::= <exp> <elementos> | e

inicio ='''<!DOCTYPE html>
<html>
    
<head>
    <meta charset="UTF-8">
    <title>Actividad Integradora 3.2</title>
    <link rel="stylesheet" href="resalta_sintaxis.css">
</head>

<body>

'''
final = '''
</body>

</html>'''

import sys
import obten_tokenAI as scanner

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    print("TOKEN:", scanner.lexema)
    if token == tokenEsperado:
        #scanner.lexema = ""
        token = scanner.obten_token()
    else:
        error("Token Equivocado")

# Funcion principal: implementa el analisis sintactico
def parser():
    global token
    token = scanner.obten_token() # inicializa con el primer token
    print("Vamos a PROG")
    prog()

def prog():
    if token == scanner.IDE or token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR or\
        token == scanner.IZQ:
        print("Vamos a EXP")
        exp()
        print("Vamos a PROG")
        prog()
    elif token == scanner.END:
        print("Expresion bien construida")
    else:
        print("Expresion mal construida")

def exp():
    if token == scanner.IDE or token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR:
        print("Vamos a ATOMO")
        atomo()
    elif token == scanner.IZQ:
        print("Vamos A LISTA")
        lista()
    else:
        error("Expresion mal iniciada")

def atomo():
    if token == scanner.IDE:
        match(token)
    elif token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR:
        print("Vamos a CONSTANTE")
        constante()
    else:
        error("Expresion mal iniciada")

def constante():
    if token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR:
        match(token)
    else:
        error("Expresion mal iniciada")

def lista():
    if token == scanner.IZQ:
        match(token)
        print("Vamos a ELEMENTOS")
        elementos()
        match(scanner.DER)
    else:
        error("Expresion mal iniciada")

def elementos():
    if token == scanner.IDE or token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR or\
        token == scanner.IZQ:
        print("Vamos a EXP")
        exp()
        print("Vamos a ELEMENTOS")
        elementos()

def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)

# def createHTML(token, lexema):
#     html = open("parser.html", "w")
#     html.write(inicio)
