# lexer.py

import ply.lex as lex

# Reserved words
RESERVED = {
    "if": "SI",
    "else": "SINO",
    "while": "MIENTRAS",
    "for": "PARA",
    "return": "RETORNAR",
    "int": "ENTERO",
    "float": "FLOTANTE",
    "string": "CADENA",
    "bool": "BOOLEANO",
    "true": "VERDADERO",
    "false": "FALSO",
}

# Token list
tokens = [
    "ID",
    "NUMERO",
    "LITERAL_CADENA",
    "MAS",
    "MENOS",
    "POR",
    "DIVIDIR",
    "ASIGNAR",
    "IGUAL",
    "DISTINTO",
    "MENOR",
    "MENOR_IGUAL",
    "MAYOR",
    "MAYOR_IGUAL",
    "PAREN_IZQ",
    "PAREN_DER",
    "LLAVE_IZQ",
    "LLAVE_DER",
    "PUNTO_Y_COMA",
    "COMA",
] + list(RESERVED.values())

# Regular expression rules for simple tokens
t_IGUAL = r"=="
t_DISTINTO = r"!="
t_MENOR_IGUAL = r"<="
t_MAYOR_IGUAL = r">="
t_ASIGNAR = r"="
t_MENOR = r"<"
t_MAYOR = r">"
t_MAS = r"\+"
t_MENOS = r"-"
t_POR = r"\*"
t_DIVIDIR = r"/"
t_PAREN_IZQ = r"\("
t_PAREN_DER = r"\)"
t_LLAVE_IZQ = r"\{"
t_LLAVE_DER = r"\}"
t_PUNTO_Y_COMA = r";"
t_COMA = r","

# Ignored characters (spaces and tabs)
t_ignore = " \t"


def t_LITERAL_CADENA(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = t.value[1:-1]
    return t


def t_NUMERO(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = RESERVED.get(t.value, "ID")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_comment(t):
    r"//.*"
    pass


def t_multiline_comment(t):
    r"/\*([\s\S]*?)\*/"
    t.lexer.lineno += t.value.count("\n")
    pass


def t_error(t):
    # Record the error and skip one character.
    t.lexer.errors.append((t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)


def build_lexer():
    lexer = lex.lex()
    lexer.errors = []
    return lexer
