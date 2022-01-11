# Marcelo Márquez Murillo - A01720588

import sys
import parserAI as parser # Importamos el codigo de parser para enviarle los espacios

# Tokens
INT = 100 # Número entero
FLT = 101 # Número de punto flotante
IDE = 102 # Identificador
STR = 103 # String
IZQ = 104 # Parentesis IZQ (Delim)
DER = 105 # Parentesis DER (Delim)
BOL = 106 # Booleanos
END = 107 # Fin de la entrada
ERR = 200 # Error léxico: palabra desconocida

# Token especial para Espacios
ESP = 108

#    num    (    )  esp    .    #    tf  ch    "  raro   $
MT = [[1, IZQ, DER, ESP,   7,   6,   4,   4,   5,   7, END],   # Edo 0 - edo inicial
      [1, INT, INT, INT,   2,   7,   7,   7,   7,   7, INT],   # Edo 1 - digitos entertos
      [3, ERR, ERR, ERR,   7,   7,   7,   7,   7,   7, ERR],   # Edo 2 - primer decimal flotante
      [3, FLT, FLT, FLT,   7,   7,   7,   7,   7,   7, FLT],   # Edo 3 - decimales restantes
      [7, IDE, IDE, IDE,   7,   7,   4,   4,   7,   7, IDE],   # Edo 4 - simbolo
      [5,   5,   5,   5,   5,   7,   5,   5, STR,   7,   7],   # Edo 5 - string
      [7,   7,   7, ERR,   7,   7, BOL,   7,   7,   7,   7],   # Edo 6 - booleanos
      [7, ERR, ERR, ERR,   7,   7,   7,   7,   7,   7,   7]]   # Edo 7 - Error

def filtro(c):
    # Regresa el numero de columna asociado al tipo de caracter dado(c)
    if c == '0' or c == '1' or c == '2' or \
       c == '3' or c == '4' or c == '5' or \
       c == '6' or c == '7' or c == '8' or c == '9': # digitos
        return 0

    elif c == '(': # parentesis IZQ
        return 1
    
    elif c == ')': # parentesis DER
        return 2

        # espacio    tab            newline         otro 
    elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13: # blancos
        return 3

    elif c == '.': # punto
        return 4

    elif c == '#': #inicio bool
        return 5

    elif c == 't' or c == 'f': # true/false o caracter
        return 6

    elif c == 'a' or c == 'b' or c == 'c' or c == 'd' or c == 'e' or \
         c == 'g' or c == 'h' or c == 'i' or c == 'j' or c == 'k' or \
         c == 'l' or c == 'm' or c == 'n' or c == 'o' or c == 'p' or \
         c == 'q' or c == 'r' or c == 's' or c == 'u' or c == 'v' or \
         c == 'w' or c == 'x' or  c == 'y' or c == 'z': # caracter
        return 7
    
    elif c == '"': # string
        return 8
    
    elif c == '$': # fin de entrada
        return 10

    else: # caracter raro
        return 9

_c = None # Siguiente caracter
_leer = True # Indica si se requiere leer un caracter de la entrada estándar
errorLex = False # Indica si hubo errores lexicos, si hay, cerramos el Script

def obten_token():
    # Implementa un analizador lexico
    global _c, _leer, errorLex
    edo = 0 # numero de estado en el automata
    global lexema # Hacemos el lexema global para que el parser pueda recibirlos
    lexema = "" # palabra que genera el token
    while (True):
        while edo < 100: # mientras que el estado no sea ACEPTOR o ERROR
            if _leer: _c = sys.stdin.read(1)
            else: _leer = True
            edo = MT[edo][filtro(_c)]
            if edo < 100 and edo != 0: lexema += _c

        if edo == INT:
            _leer = False # ya se leyo el siguiente caracter (delim)
            #print("Num Entero:", lexema, INT)
            return INT

        elif edo == FLT:
            _leer = False # ya se leyo el siguiente caracter (delim)
            #print("Num Flotante:", lexema, FLT)
            return FLT

        elif edo == IDE:
            _leer = False # ya se leyo el siguiente caracter (delim)
            #print("Simbolo:", lexema, IDE)
            return IDE

        elif edo == STR:
            lexema += _c  # el ultimo caracter forma el lexema
            #print("String:", lexema, STR)
            return STR

        elif edo == IZQ:
            lexema += _c  # el ultimo caracter forma el lexema
            #print("Parentesis IZQ:", lexema, IZQ)
            return IZQ

        elif edo == DER:
            lexema += _c  # el ultimo caracter forma el lexema
            #print("Parentesis DER:", lexema, DER)
            return DER

        elif edo == BOL:
            lexema += _c  # el ultimo caracter forma el lexema
            #print("Booleano:", lexema, BOL)
            return BOL

        elif edo == END:
            #print("Fin de expresion")
            return END

        elif edo == ESP:
            lexema += _c  # el ultimo caracter forma el lexema
            edo = 0 # Dado a que en vez de que el esp actue solo regrese a 0, manualmente lo movemos a cero
            parser.agregarEspacios(lexema) # Enviamos al codigo del parser los espacios para que ahi se puedan escribir al archivo
            lexema = "" # Vaciamos el lexema para que el proximo lexema no reciba espacios

        else:
            _leer = False # el ultimo caracter no es raro
            print("ERROR LEXICO! palabra ilegal:", lexema)
            parser.createHTML(ERR, lexema)
            edo = 0
            lexema = ""
            errorLex = True


