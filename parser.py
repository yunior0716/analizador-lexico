import ply.yacc as yacc

from lexer import build_lexer, tokens


class SyntaxParser:
    tokens = tokens

    precedence = (
        ("left", "IGUAL", "DISTINTO"),
        ("left", "MENOR", "MENOR_IGUAL", "MAYOR", "MAYOR_IGUAL"),
        ("left", "MAS", "MENOS"),
        ("left", "POR", "DIVIDIR"),
        ("right", "UMINUS"),
    )

    def __init__(self):
        self.syntax_errors = []
        self.parser = yacc.yacc(module=self, write_tables=False, debug=False)

    def parse(self, data):
        self.syntax_errors = []
        lexer = build_lexer()
        ast = self.parser.parse(data, lexer=lexer)
        return {
            "arbol": ast,
            "errores_lexicos": lexer.errors,
            "errores_sintacticos": self.syntax_errors,
        }

    def p_program(self, p):
        "program : statement_list"
        p[0] = {"tipo": "programa", "cuerpo": p[1]}

    def p_statement_list_recursive(self, p):
        "statement_list : statement_list statement"
        p[0] = p[1] + [p[2]]

    def p_statement_list_empty(self, p):
        "statement_list : empty"
        p[0] = []

    def p_statement(self, p):
        """statement : declaration_stmt
        | assignment_stmt
        | if_stmt
        | while_stmt
        | for_stmt
        | return_stmt
        | block
        | expression_stmt"""
        p[0] = p[1]

    def p_block(self, p):
        "block : LLAVE_IZQ statement_list LLAVE_DER"
        p[0] = {"tipo": "bloque", "cuerpo": p[2]}

    def p_declaration_stmt(self, p):
        "declaration_stmt : type_spec ID opt_initializer PUNTO_Y_COMA"
        p[0] = {
            "tipo": "declaracion",
            "tipo_dato": p[1],
            "identificador": p[2],
            "valor": p[3],
        }

    def p_opt_initializer(self, p):
        """opt_initializer : ASIGNAR expression
        | empty"""
        p[0] = p[2] if len(p) == 3 else None

    def p_assignment_stmt(self, p):
        "assignment_stmt : ID ASIGNAR expression PUNTO_Y_COMA"
        p[0] = {"tipo": "asignacion", "identificador": p[1], "valor": p[3]}

    def p_expression_stmt(self, p):
        "expression_stmt : expression PUNTO_Y_COMA"
        p[0] = {"tipo": "sentencia_expresion", "expresion": p[1]}

    def p_if_stmt(self, p):
        "if_stmt : SI PAREN_IZQ expression PAREN_DER statement else_clause"
        p[0] = {
            "tipo": "si",
            "condicion": p[3],
            "entonces": p[5],
            "sino": p[6],
        }

    def p_else_clause(self, p):
        """else_clause : SINO statement
        | empty"""
        p[0] = p[2] if len(p) == 3 else None

    def p_while_stmt(self, p):
        "while_stmt : MIENTRAS PAREN_IZQ expression PAREN_DER statement"
        p[0] = {"tipo": "mientras", "condicion": p[3], "cuerpo": p[5]}

    def p_for_stmt(self, p):
        "for_stmt : PARA PAREN_IZQ for_init PUNTO_Y_COMA for_cond PUNTO_Y_COMA for_update PAREN_DER statement"
        p[0] = {
            "tipo": "para",
            "inicializacion": p[3],
            "condicion": p[5],
            "actualizacion": p[7],
            "cuerpo": p[9],
        }

    def p_for_init(self, p):
        """for_init : for_declaration
        | for_assignment
        | empty"""
        p[0] = p[1]

    def p_for_declaration(self, p):
        "for_declaration : type_spec ID opt_initializer"
        p[0] = {
            "tipo": "declaracion",
            "tipo_dato": p[1],
            "identificador": p[2],
            "valor": p[3],
        }

    def p_for_assignment(self, p):
        "for_assignment : ID ASIGNAR expression"
        p[0] = {"tipo": "asignacion", "identificador": p[1], "valor": p[3]}

    def p_for_cond(self, p):
        """for_cond : expression
        | empty"""
        p[0] = p[1]

    def p_for_update(self, p):
        """for_update : for_assignment
        | empty"""
        p[0] = p[1]

    def p_return_stmt(self, p):
        "return_stmt : RETORNAR opt_expression PUNTO_Y_COMA"
        p[0] = {"tipo": "retornar", "valor": p[2]}

    def p_opt_expression(self, p):
        """opt_expression : expression
        | empty"""
        p[0] = p[1]

    def p_type_spec(self, p):
        """type_spec : ENTERO
        | FLOTANTE
        | CADENA
        | BOOLEANO"""
        p[0] = p[1]

    def p_expression_binary(self, p):
        """expression : expression MAS expression
        | expression MENOS expression
        | expression POR expression
        | expression DIVIDIR expression
        | expression IGUAL expression
        | expression DISTINTO expression
        | expression MENOR expression
        | expression MENOR_IGUAL expression
        | expression MAYOR expression
        | expression MAYOR_IGUAL expression"""
        p[0] = {
            "tipo": "operacion_binaria",
            "operador": p[2],
            "izquierda": p[1],
            "derecha": p[3],
        }

    def p_expression_group(self, p):
        "expression : PAREN_IZQ expression PAREN_DER"
        p[0] = p[2]

    def p_expression_unary(self, p):
        "expression : MENOS expression %prec UMINUS"
        p[0] = {"tipo": "operacion_unaria", "operador": "-", "operando": p[2]}

    def p_expression_id(self, p):
        "expression : ID"
        p[0] = {"tipo": "identificador", "nombre": p[1]}

    def p_expression_number(self, p):
        "expression : NUMERO"
        p[0] = {"tipo": "numero", "valor": p[1]}

    def p_expression_string(self, p):
        "expression : LITERAL_CADENA"
        p[0] = {"tipo": "cadena", "valor": p[1]}

    def p_expression_boolean(self, p):
        """expression : VERDADERO
        | FALSO"""
        p[0] = {"tipo": "booleano", "valor": p.slice[1].type == "VERDADERO"}

    def p_empty(self, p):
        "empty :"
        p[0] = None

    def p_error(self, p):
        if self.syntax_errors:
            return

        if p:
            self.syntax_errors.append(
                {
                    "mensaje": f"Token inesperado '{p.value}'",
                    "linea": p.lineno,
                    "posicion": p.lexpos,
                }
            )
        else:
            self.syntax_errors.append(
                {
                    "mensaje": "Fin de entrada inesperado",
                    "linea": 0,
                    "posicion": 0,
                }
            )


def build_parser():
    return SyntaxParser()
