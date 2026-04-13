# executor.py
# Ejecutor de codigo intermedio - convierte TAC a JavaScript y lo ejecuta.

import os
import subprocess
import re
from typing import List


class CodeExecutor:
    """Convierte codigo intermedio (TAC) a JavaScript ejecutable."""

    def __init__(self):
        self.js_code = []
        self.temp_vars = set()
        self.labels = {}
        self.declared_vars = set()  # Rastrear variables ya declaradas

    def execute_intermediate_code(self, intermediate_code: List[str], output_dir: str = None):
        """
        Convierte codigo TAC a JavaScript y lo ejecuta.

        Args:
            intermediate_code: Lista de instrucciones TAC
            output_dir: Directorio donde guardar el archivo .js (por defecto: directorio actual)

        Returns:
            dict con 'success', 'js_file', 'output', 'error'
        """
        if not intermediate_code:
            return {
                'success': False,
                'js_file': None,
                'output': '',
                'error': 'No hay codigo intermedio para ejecutar.'
            }

        # Convertir TAC a JavaScript
        try:
            js_code = self._convert_tac_to_js(intermediate_code)
        except Exception as e:
            return {
                'success': False,
                'js_file': None,
                'output': '',
                'error': f'Error convirtiendo TAC a JavaScript: {str(e)}'
            }

        # Guardar archivo JavaScript
        if output_dir is None:
            output_dir = os.getcwd()

        js_file = os.path.join(output_dir, 'programa_generado.js')

        try:
            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(js_code)
        except Exception as e:
            return {
                'success': False,
                'js_file': js_file,
                'output': '',
                'error': f'Error guardando archivo JavaScript: {str(e)}'
            }

        # Ejecutar con Node.js
        try:
            result = subprocess.run(
                ['node', js_file],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8'
            )

            return {
                'success': result.returncode == 0,
                'js_file': js_file,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else ''
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'js_file': js_file,
                'output': '',
                'error': 'Timeout: El programa tardo mas de 10 segundos en ejecutarse.'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'js_file': js_file,
                'output': '',
                'error': 'Node.js no esta instalado o no se encuentra en el PATH.'
            }
        except Exception as e:
            return {
                'success': False,
                'js_file': js_file,
                'output': '',
                'error': f'Error ejecutando JavaScript: {str(e)}'
            }

    def _convert_tac_to_js(self, tac_lines: List[str]) -> str:
        """Convierte codigo de tres direcciones a JavaScript."""
        self.js_code = []
        self.temp_vars = set()
        self.labels = {}
        self.declared_vars = set()  # Reset para cada conversion

        # Limpiar y filtrar lineas vacias
        cleaned_lines = [line.strip() for line in tac_lines if line.strip()]

        # Header del archivo JavaScript
        self.js_code.append('// JavaScript generado automaticamente desde codigo intermedio')
        self.js_code.append('// Ejecutar con: node programa_generado.js')
        self.js_code.append('')

        # Analizar patrones de control de flujo y convertir directamente
        self._analyze_and_convert_control_flow(cleaned_lines)

        # Declarar variables temporales al inicio si las hay
        if self.temp_vars:
            temp_declarations = 'let ' + ', '.join(sorted(self.temp_vars)) + ';'
            self.js_code.insert(3, temp_declarations)
            self.js_code.insert(4, '')

        return '\n'.join(self.js_code)

    def _analyze_and_convert_control_flow(self, lines: List[str]):
        """Analiza y convierte estructuras de control de flujo."""
        i = 0
        while i < len(lines):
            line = lines[i]

            # Declaraciones y asignaciones simples
            if ' = ' in line and not line.startswith('SI_FALSO') and not line.startswith('IR_A'):
                js_line = self._convert_assignment(line)
                self.js_code.append(js_line)
                i += 1
                continue

            # Reconocer patron IF: SI_FALSO cond IR_A label
            if line.startswith('SI_FALSO') and i < len(lines) - 1:
                if_result = self._convert_if_structure(lines, i)
                if if_result:
                    js_lines, next_i = if_result
                    self.js_code.extend(js_lines)
                    i = next_i
                    continue

            # Reconocer patron WHILE: label: ... SI_FALSO cond IR_A end ... IR_A label
            if line.endswith(':'):
                while_result = self._convert_while_structure(lines, i)
                if while_result:
                    js_lines, next_i = while_result
                    self.js_code.extend(js_lines)
                    i = next_i
                    continue

            # Return
            if line.startswith('RETORNAR'):
                js_line = self._convert_return(line)
                self.js_code.append(js_line)
                i += 1
                continue

            # Saltar etiquetas solas y comandos IR_A
            if line.endswith(':') or line.startswith('IR_A'):
                i += 1
                continue

            # Linea no reconocida
            self.js_code.append(f'// TAC: {line}')
            i += 1

    def _convert_if_structure(self, lines: List[str], start_idx: int):
        """Convierte estructura if desde TAC."""
        if start_idx >= len(lines):
            return None

        si_falso_line = lines[start_idx]
        if not si_falso_line.startswith('SI_FALSO'):
            return None

        # Extraer condicion y etiqueta
        parts = si_falso_line.split()
        if len(parts) < 4:
            return None

        condition = parts[1]
        end_label = parts[3]

        # Buscar el cuerpo del if (hasta encontrar la etiqueta de fin)
        then_body = []
        i = start_idx + 1
        found_else = False
        else_body = []

        while i < len(lines):
            line = lines[i]

            # Encontrar etiqueta de fin
            if line == f"{end_label}:":
                break

            # Encontrar IR_A seguido de etiqueta (indica else)
            if line.startswith('IR_A') and i + 1 < len(lines) and lines[i + 1] == f"{end_label.replace('1', '2' if '1' in end_label else '1')}:":
                # Buscar else body despues de la etiqueta
                found_else = True
                i += 2  # Saltar IR_A y etiqueta else
                while i < len(lines) and not lines[i] == f"{end_label}:":
                    if lines[i].strip() and not lines[i].endswith(':'):
                        else_body.append(self._convert_tac_line_simple(lines[i]))
                    i += 1
                break

            # Agregar al cuerpo del then
            if line.strip() and not line.endswith(':') and not line.startswith('IR_A'):
                then_body.append(self._convert_tac_line_simple(line))

            i += 1

        # Generar codigo JavaScript
        js_lines = []
        js_condition = self._convert_expression(condition)
        js_lines.append(f'if ({js_condition}) {{')

        for body_line in then_body:
            js_lines.append(f'    {body_line}')

        if found_else and else_body:
            js_lines.append('} else {')
            for else_line in else_body:
                js_lines.append(f'    {else_line}')

        js_lines.append('}')

        return js_lines, i + 1

    def _convert_while_structure(self, lines: List[str], start_idx: int):
        """Convierte estructura while desde TAC."""
        if start_idx >= len(lines) or not lines[start_idx].endswith(':'):
            return None

        start_label = lines[start_idx].rstrip(':')

        # Buscar patron while: label: ... SI_FALSO cond IR_A end ... IR_A label
        i = start_idx + 1
        condition = None
        body_lines = []

        # Buscar SI_FALSO
        while i < len(lines):
            line = lines[i]
            if line.startswith('SI_FALSO'):
                parts = line.split()
                if len(parts) >= 4:
                    condition = parts[1]
                    break
            # Agregar al cuerpo si no es SI_FALSO
            if line.strip() and not line.endswith(':') and not line.startswith('SI_FALSO'):
                body_lines.append(self._convert_tac_line_simple(line))
            i += 1

        if not condition:
            return None

        # Recopilar el resto del cuerpo del while (despues del SI_FALSO)
        i += 1
        while i < len(lines):
            line = lines[i]
            if line.startswith(f'IR_A {start_label}'):
                break
            if line.strip() and not line.endswith(':'):
                body_lines.append(self._convert_tac_line_simple(line))
            i += 1

        # Generar codigo JavaScript
        js_lines = []
        js_condition = self._convert_expression(condition)
        js_lines.append(f'while ({js_condition}) {{')

        for body_line in body_lines:
            js_lines.append(f'    {body_line}')

        js_lines.append('}')

        return js_lines, i + 1

    def _convert_assignment(self, line: str) -> str:
        """Convierte asignacion TAC a JavaScript."""
        left, right = line.split(' = ', 1)
        left = left.strip()
        right = right.strip()

        # Registrar variables temporales
        if left.startswith('t') and left[1:].isdigit():
            self.temp_vars.add(left)
            return f'{left} = {self._convert_expression(right)};'
        else:
            # Para variables normales, usar let solo la primera vez
            if left not in self.declared_vars:
                self.declared_vars.add(left)
                return f'let {left} = {self._convert_expression(right)};'
            else:
                # Variable ya declarada, solo asignar
                return f'{left} = {self._convert_expression(right)};'

    def _convert_tac_line_simple(self, line: str) -> str:
        """Convierte una linea TAC simple (sin control de flujo)."""
        if ' = ' in line:
            return self._convert_assignment(line)
        elif line.startswith('RETORNAR'):
            return self._convert_return(line)
        else:
            return f'// {line}'

    def _convert_return(self, line: str) -> str:
        """Convierte RETORNAR a JavaScript."""
        parts = line.split()
        if len(parts) > 1:
            value = parts[1]
            return f'return {self._convert_expression(value)};'
        else:
            return 'return;'

    def _convert_expression(self, expr: str) -> str:
        """Convierte una expresion TAC a JavaScript."""
        expr = expr.strip()

        # Literales string
        if expr.startswith('"') and expr.endswith('"'):
            return expr

        # Booleanos
        if expr == 'verdadero':
            return 'true'
        elif expr == 'falso':
            return 'false'

        # Numeros
        if expr.replace('.', '').replace('-', '').isdigit():
            return expr

        # Operaciones binarias: a + b, x >= 5
        binary_ops = ['>=', '<=', '!=', '==', '>', '<', '+', '-', '*', '/']
        for op in binary_ops:
            if f' {op} ' in expr:
                left, right = expr.split(f' {op} ', 1)
                left_js = self._convert_expression(left.strip())
                right_js = self._convert_expression(right.strip())
                return f'{left_js} {op} {right_js}'

        # Variables (incluye temporales)
        return expr


def build_executor():
    return CodeExecutor()