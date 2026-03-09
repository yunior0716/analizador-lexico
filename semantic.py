# semantic.py
class SemanticAnalyzer:

    def __init__(self):
        self.errors = []
        self.scopes = [{}]

    def _enter_scope(self):
        self.scopes.append({})

    def _exit_scope(self):
        self.scopes.pop()

    def _declare(self, nombre, tipo):
        """Registra una variable en el scope actual. Error si ya existe."""
        scope_actual = self.scopes[-1]
        if nombre in scope_actual:
            self._error(f"Variable '{nombre}' ya fue declarada en este bloque")
        else:
            scope_actual[nombre] = tipo

    def _lookup(self, nombre):
        """Busca una variable del scope mas interno al mas externo.
        Retorna el tipo si la encuentra, o None si no existe."""
        for scope in reversed(self.scopes):
            if nombre in scope:
                return scope[nombre]
        return None

    def _error(self, mensaje):
        self.errors.append({"mensaje": mensaje})

    def analyze(self, ast):
        """Recibe el AST del parser y devuelve una lista de errores semanticos."""
        self.errors = []
        self.scopes = [{}]
        if ast is not None:
            self._visit(ast)
        return self.errors

    def _visit(self, node):
        if node is None:
            return None

        tipo_nodo = node.get("tipo")

        if tipo_nodo == "programa":
            return self._visit_programa(node)
        elif tipo_nodo == "bloque":
            return self._visit_bloque(node)
        elif tipo_nodo == "declaracion":
            return self._visit_declaracion(node)
        elif tipo_nodo == "asignacion":
            return self._visit_asignacion(node)
        elif tipo_nodo == "si":
            return self._visit_si(node)
        elif tipo_nodo == "mientras":
            return self._visit_mientras(node)
        elif tipo_nodo == "para":
            return self._visit_para(node)
        elif tipo_nodo == "retornar":
            return self._visit_retornar(node)
        elif tipo_nodo == "sentencia_expresion":
            return self._visit(node["expresion"])
        elif tipo_nodo == "operacion_binaria":
            return self._visit_operacion_binaria(node)
        elif tipo_nodo == "operacion_unaria":
            return self._visit_operacion_unaria(node)
        elif tipo_nodo == "identificador":
            return self._visit_identificador(node)
        elif tipo_nodo == "numero":
            # Retorna "float" si tiene decimales, "int" si es entero
            return "float" if isinstance(node["valor"], float) else "int"
        elif tipo_nodo == "cadena":
            return "string"
        elif tipo_nodo == "booleano":
            return "bool"

        return None


    def _visit_programa(self, node):
        for sentencia in node["cuerpo"]:
            self._visit(sentencia)

    def _visit_bloque(self, node):
        self._enter_scope()
        for sentencia in node["cuerpo"]:
            self._visit(sentencia)
        self._exit_scope()

    def _visit_declaracion(self, node):
        nombre = node["identificador"]
        tipo_declarado = self._token_a_tipo(node["tipo_dato"])

        # Registrar la variable en la tabla de simbolos
        self._declare(nombre, tipo_declarado)

        # Si tiene valor inicial, verificar que el tipo sea compatible
        if node["valor"] is not None:
            tipo_valor = self._visit(node["valor"])
            if tipo_valor is not None:
                self._verificar_compatibilidad(tipo_declarado, tipo_valor, nombre)

    def _visit_asignacion(self, node):
        nombre = node["identificador"]
        tipo_declarado = self._lookup(nombre)

        if tipo_declarado is None:
            self._error(f"Variable '{nombre}' no ha sido declarada")
        else:
            tipo_valor = self._visit(node["valor"])
            if tipo_valor is not None:
                self._verificar_compatibilidad(tipo_declarado, tipo_valor, nombre)

    def _visit_si(self, node):
        self._visit(node["condicion"])
        self._visit(node["entonces"])
        if node["sino"] is not None:
            self._visit(node["sino"])

    def _visit_mientras(self, node):
        self._visit(node["condicion"])
        self._visit(node["cuerpo"])

    def _visit_para(self, node):
        # El for crea su propio scope para la variable de inicializacion
        self._enter_scope()
        if node["inicializacion"]:
            self._visit(node["inicializacion"])
        if node["condicion"]:
            self._visit(node["condicion"])
        if node["actualizacion"]:
            self._visit(node["actualizacion"])
        self._visit(node["cuerpo"])
        self._exit_scope()

    def _visit_retornar(self, node):
        if node["valor"] is not None:
            self._visit(node["valor"])

    def _visit_identificador(self, node):
        nombre = node["nombre"]
        tipo = self._lookup(nombre)
        if tipo is None:
            self._error(f"Variable '{nombre}' no ha sido declarada")
        return tipo

    def _visit_operacion_binaria(self, node):
        op = node["operador"]
        tipo_izq = self._visit(node["izquierda"])
        tipo_der = self._visit(node["derecha"])

        # Operadores de comparacion: siempre devuelven bool
        if op in ("==", "!=", "<", "<=", ">", ">="):
            if tipo_izq and tipo_der and tipo_izq != tipo_der:
                self._error(
                    f"Comparacion entre tipos incompatibles: '{tipo_izq}' {op} '{tipo_der}'"
                )
            return "bool"

        # Operadores aritmeticos: +, -, *, /
        if op in ("+", "-", "*", "/"):
            # Caso especial: concatenacion de strings con +
            if op == "+" and tipo_izq == "string" and tipo_der == "string":
                return "string"
            # Para los demas casos, ambos deben ser numericos
            if tipo_izq and tipo_der:
                if tipo_izq not in ("int", "float") or tipo_der not in ("int", "float"):
                    self._error(
                        f"Operacion '{op}' no es valida entre '{tipo_izq}' y '{tipo_der}'"
                    )
                    return None
                # Si alguno es float, el resultado es float
                return "float" if "float" in (tipo_izq, tipo_der) else "int"

        return None

    def _visit_operacion_unaria(self, node):
        tipo = self._visit(node["operando"])
        if tipo is not None and tipo not in ("int", "float"):
            self._error(f"Operador '-' no es valido para el tipo '{tipo}'")
        return tipo


    def _token_a_tipo(self, tipo_dato):
        """Convierte el nombre del token del lexer al nombre interno del tipo."""
        mapping = {
            "int":    "int",
            "float":  "float",
            "string": "string",
            "bool":   "bool",
        }
        return mapping.get(tipo_dato, tipo_dato)

    def _verificar_compatibilidad(self, tipo_declarado, tipo_valor, nombre):
        """Verifica que el tipo del valor sea compatible con el tipo declarado."""
        # Mismo tipo: ok
        if tipo_declarado == tipo_valor:
            return
        # Asignar int a float esta permitido (pero no al reves)
        if tipo_declarado == "float" and tipo_valor == "int":
            return
        # Cualquier otro caso es un error
        self._error(
            f"Tipo incompatible para '{nombre}': "
            f"se esperaba '{tipo_declarado}', se encontro '{tipo_valor}'"
        )


def build_semantic_analyzer():
    return SemanticAnalyzer()
