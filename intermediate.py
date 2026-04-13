# intermediate.py
# Generador de codigo intermedio (Three-Address Code) a partir del AST.


class IntermediateCodeGenerator:
    """Recorre el AST y genera codigo intermedio de tres direcciones."""

    def __init__(self):
        self._temp_count = 0
        self._label_count = 0
        self.code = []

    def _new_temp(self):
        self._temp_count += 1
        return f"t{self._temp_count}"

    def _new_label(self):
        self._label_count += 1
        return f"L{self._label_count}"

    def _emit(self, instruction):
        self.code.append(instruction)

    def generate(self, ast):
        """Recibe el AST del parser y devuelve una lista de instrucciones de tres direcciones."""
        self.code = []
        self._temp_count = 0
        self._label_count = 0
        if ast is not None:
            self._visit(ast)
        return self.code

    def _visit(self, node):
        if node is None:
            return None

        tipo = node.get("tipo")

        if tipo == "programa":
            return self._visit_programa(node)
        elif tipo == "bloque":
            return self._visit_bloque(node)
        elif tipo == "declaracion":
            return self._visit_declaracion(node)
        elif tipo == "asignacion":
            return self._visit_asignacion(node)
        elif tipo == "si":
            return self._visit_si(node)
        elif tipo == "mientras":
            return self._visit_mientras(node)
        elif tipo == "para":
            return self._visit_para(node)
        elif tipo == "retornar":
            return self._visit_retornar(node)
        elif tipo == "sentencia_expresion":
            return self._visit(node["expresion"])
        elif tipo == "operacion_binaria":
            return self._visit_operacion_binaria(node)
        elif tipo == "operacion_unaria":
            return self._visit_operacion_unaria(node)
        elif tipo == "identificador":
            return node["nombre"]
        elif tipo == "numero":
            return str(node["valor"])
        elif tipo == "cadena":
            return f'"{node["valor"]}"'
        elif tipo == "booleano":
            return "verdadero" if node["valor"] else "falso"

        return None

    def _visit_programa(self, node):
        for stmt in node["cuerpo"]:
            self._visit(stmt)

    def _visit_bloque(self, node):
        for stmt in node["cuerpo"]:
            self._visit(stmt)

    def _visit_declaracion(self, node):
        nombre = node["identificador"]
        if node["valor"] is not None:
            valor = self._visit(node["valor"])
            self._emit(f"{nombre} = {valor}")
        else:
            self._emit(f"{nombre} = 0")

    def _visit_asignacion(self, node):
        nombre = node["identificador"]
        valor = self._visit(node["valor"])
        self._emit(f"{nombre} = {valor}")

    def _visit_si(self, node):
        cond = self._visit(node["condicion"])
        label_else = self._new_label()
        label_fin = self._new_label()

        if node["sino"] is not None:
            self._emit(f"SI_FALSO {cond} IR_A {label_else}")
            self._visit(node["entonces"])
            self._emit(f"IR_A {label_fin}")
            self._emit(f"{label_else}:")
            self._visit(node["sino"])
            self._emit(f"{label_fin}:")
        else:
            self._emit(f"SI_FALSO {cond} IR_A {label_fin}")
            self._visit(node["entonces"])
            self._emit(f"{label_fin}:")

    def _visit_mientras(self, node):
        label_inicio = self._new_label()
        label_fin = self._new_label()

        self._emit(f"{label_inicio}:")
        cond = self._visit(node["condicion"])
        self._emit(f"SI_FALSO {cond} IR_A {label_fin}")
        self._visit(node["cuerpo"])
        self._emit(f"IR_A {label_inicio}")
        self._emit(f"{label_fin}:")

    def _visit_para(self, node):
        if node["inicializacion"]:
            self._visit(node["inicializacion"])

        label_inicio = self._new_label()
        label_fin = self._new_label()

        self._emit(f"{label_inicio}:")
        if node["condicion"]:
            cond = self._visit(node["condicion"])
            self._emit(f"SI_FALSO {cond} IR_A {label_fin}")

        self._visit(node["cuerpo"])

        if node["actualizacion"]:
            self._visit(node["actualizacion"])

        self._emit(f"IR_A {label_inicio}")
        self._emit(f"{label_fin}:")

    def _visit_retornar(self, node):
        if node["valor"] is not None:
            valor = self._visit(node["valor"])
            self._emit(f"RETORNAR {valor}")
        else:
            self._emit("RETORNAR")

    def _visit_operacion_binaria(self, node):
        izq = self._visit(node["izquierda"])
        der = self._visit(node["derecha"])
        temp = self._new_temp()
        self._emit(f"{temp} = {izq} {node['operador']} {der}")
        return temp

    def _visit_operacion_unaria(self, node):
        operando = self._visit(node["operando"])
        temp = self._new_temp()
        self._emit(f"{temp} = -{operando}")
        return temp


def build_intermediate_generator():
    return IntermediateCodeGenerator()
