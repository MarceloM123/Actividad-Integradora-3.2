# Marcelo Márquez Murillo - A01720588

# Los prints fueron utilizados como debuggers

# Inicio de cada codigo HTML
inicio ='''<!DOCTYPE html> 
<html>
    
<head>
    <meta charset="UTF-8">
    <title>Actividad Integradora 3.2</title>
    <link rel="stylesheet" href="resalta_sintaxis.css">
</head>

<body>

'''
# Final de cada codigo HTML
final = '''
</body>

</html>'''

import sys
import obten_tokenAI as scanner # Importamos el codigo de obten_token

# Abrimos el archivo HTML y le agregamos el inicio
html = open("parser.html", "w")
html.write(inicio)

# Booleano para saber si el final ($) ya fue escrito o no para no ser repetido
dlFinal = False

# Bool para revisar si hay error sintactico
errorSin = False

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    if token == tokenEsperado:
        #print("HTML: Escribimos token y lexema a HTML")
        createHTML(token, scanner.lexema) # Cuando hacen match, enviamos el token y lexema para que puedan ser escritos en el HTML
        token = scanner.obten_token()
        #print("LEXICO: Conseguimos siguiente token:", token, "lexema:", scanner.lexema)
    else:
        #print("Vamos a errorSintactico dentro MATCH")
        errorSintactico()

# Funcion principal: implementa el analisis sintactico
def parser():
    global errorSin
    global token
    html.write('<p>\n') # Agregamos <p> para escribir un nuevo parrafo en HTML
    token = scanner.obten_token() # inicializa con el primer token
    #print("Conseguimos primer token:", token, "lexema:", scanner.lexema)
    #print("Vamos a PROG dentro PARSER")
    prog() # Empezamos en Prog

def prog():
    global dlFinal
    if token == scanner.IDE or token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR or\
        token == scanner.IZQ: # Revisamos que token esta seleccionado para saber a donde movernos
        #print("Vamos a EXP dentro PROG")
        exp()
        #print("Vamos a PROG dentro PROG")
        prog()
    elif token == scanner.END:
        createHTML(token, '$') # Enviamos manualmente el $ dado que obten_token no lo envia
        dlFinal = True
        print("Expresion terminada")
        if scanner.errorLex == True: # Revisamos si tuvimos algun error lexico por medio de errorLex
            error("") # Dado que solo estamos tomado en consideracion el error lexico
                            # llamamos error con nada que printear al igual que su segundo valor sera None
        elif errorSin == True:
            error("")
        else:
            html.write('\n</p>\n') # Agregamos </p> para cerrar el parrafo
            quit = input("Exit? Y/N: ") # Preguntamos si quiere agregar mas codigo
            if quit == 'Y' or quit == 'y':
                html.write(final) # Escribimos el final del html
                html.close() # Cerramos el archivo
                sys.exit(1) # No salimos del Script
            else:
                #print("Volvemos a correr PARSER")
                parser() # Volvemos a correr parser para seguir escribiendo
    else:
        #print("Vamos a errorSintactico dentro PROG")
        errorSintactico()

def exp():
    if token == scanner.IDE or token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR:
        # Revisamos que token esta seleccionado para saber a donde movernos
        #print("Vamos a ATOMO dentro EXP")
        atomo()
    elif token == scanner.IZQ:
        # Revisamos que token esta seleccionado para saber a donde movernos
        #print("Vamos a LISTA dentro EXP")
        lista()
    else:
        #print("Vamos a errorSintactico dentro EXP")
        errorSintactico()

def atomo():
    if token == scanner.IDE:
        match(token)
    elif token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR:
        # Revisamos que token esta seleccionado para saber a donde movernos
        #print("Vamos a CONSTANTE dentro ATOMO")
        constante()
    else:
        #print("Vamos a errorSintactico dentro ATOMO")
        errorSintactico()

def constante():
    if token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR:
        match(token)
    else:
        #print("Vamos a errorSintactico dentro CONSTANTE")
        errorSintactico()

def lista():
    if token == scanner.IZQ:
        match(token)
        #print("Vamos a ELEMENTOS dentro LISTA")
        elementos()
        if token == scanner.DER:
            match(token)
        else:
            #print("Vamos a errorSintactico dentro LISTA por (")
            errorSintactico()
    else:
        #print("Vamos a errorSintactico dentro LISTA")
        errorSintactico()

def elementos():
    global errorSin
    if token == scanner.IDE or token == scanner.INT or token == scanner.FLT or token == scanner.BOL or token == scanner.STR or\
        token == scanner.IZQ: # Revisamos que token esta seleccionado para saber a donde movernos
        #print("Vamos a EXP dentro ELEMENTOS")
        exp()
        #print("Vamos a ELEMENTOS dentro ELEMENTOS")
        elementos()
    elif token == scanner.END:
        errorSin = True
        error("No se cerro lista")
    #print("Vamos por VACIO")

def errorSintactico():
    global errorSin, token, dlFinal
    dlFinal = False
    errorSin = True
    createHTML(scanner.ERR, scanner.lexema)
    #print("Escribimos ERROR SINTACTICO:", scanner.lexema)
    #scanner.edo = 0
    token = scanner.obten_token() # Conseguir el siguiente token para poder seguir avanzando
    #print("Conseguimos proximo token para seguir avanzando:", token, "lexema:", scanner.lexema)
    #print("Regresamos a PROG dentro ERROR SINTACTICO para seguir avanzando")
    prog()
    error("Token equivocado")

def error(mensaje):
    global dlFinal
    if errorSin == True:
        if dlFinal == False:
            createHTML(scanner.END, '$')
        print("ERROR SINTACTICO:", mensaje)
        html.write('\n</p>\n')
        html.write('<p>\n<span class="err">&gt&gt ERROR SINTÁCTICO &lt&lt</span>\n</p>\n')
        # Agregamos leyenda >> ERROR SINTACTICO <<
    if scanner.errorLex == True:
        html.write('<p>\n<span class="err">&gt&gt ERROR LEXICO &lt&lt</span>\n</p>\n')
        # Agregamos leyenda >> ERROR LEXICO <<
    html.write(final)
    html.close()
    sys.exit(1)

def createHTML(token, lexema):
    if token == scanner.IDE: # Si es IDE, escribimos su <span> con su lexema
        html.write('<span class="ide">' + lexema + '</span>')
    elif token == scanner.INT: # Si es INT, escribimos su <span> con su lexema
        html.write('<span class="int">' + lexema + '</span>')
    elif token == scanner.FLT: # Si es FLT, escribimos su <span> con su lexema
        html.write('<span class="flt">' + lexema + '</span>')
    elif token == scanner.IZQ: # Si es IZQ, escribimos su <span> con su lexema
        html.write('<span class="par">' + lexema + '</span>')
    elif token == scanner.DER: # Si es DER, escribimos su <span> con su lexema
        html.write('<span class="par">' + lexema + '</span>')
    elif token == scanner.BOL: # Si es BOL, escribimos su <span> con su lexema
        html.write('<span class="bol">' + lexema + '</span>')
    elif token == scanner.STR: # Si es STR, escribimos su <span> con su lexema
        html.write('<span class="str">' + lexema + '</span>')
    elif token == scanner.END: # Si es END, escribimos su <span> con su lexema
        html.write('<span class="end">' + lexema + '</span>')
    elif token == scanner.ERR: # Si es ERR, escribimos su <span> con su lexema
        html.write('<span class="err">' + lexema + '</span>')

def agregarEspacios(espacio):
    # Para que el parser siga ignorando los espacios pero que aun los escriba en el html
    # Cuando recibimos un espacio en obten_token llamamos esta función para agregarlos
    if ord(espacio) == 9:
        html.write('&nbsp;&nbsp;&nbsp;&nbsp;')
    if ord(espacio) == 10:
        html.write('<br>\n')
    if espacio == ' ':
        html.write('&nbsp;')



