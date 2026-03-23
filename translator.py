# translator.py
# Traduce codigo JavaScript a Python.
import re


class JSTranslator:
    """Traduce codigo JavaScript basico a Python."""

    def translate(self, code):
        """Recibe codigo JS como string y devuelve el equivalente en Python."""
        code = self._block_comments(code)
        code = self._template_literals(code)

        lines = code.split('\n')
        result = []
        indent = 0

        for raw in lines:
            stripped = raw.strip()

            if not stripped:
                result.append('')
                continue

            # Llave de cierre sola → reduce indent
            if re.match(r'^\}[;,]?$', stripped):
                indent = max(0, indent - 1)
                continue

            # } else ... → reduce indent antes de traducir
            if re.match(r'^\}\s*else', stripped):
                indent = max(0, indent - 1)

            translated = self._translate_line(stripped)

            if translated:
                result.append('    ' * indent + translated)

            if stripped.endswith('{'):
                indent += 1

        return '\n'.join(result)

    # --- Transformaciones multi-linea ---

    def _block_comments(self, code):
        """/* texto */ → \"\"\" texto \"\"\""""
        return re.sub(
            r'/\*(.*?)\*/',
            lambda m: f'"""{m.group(1)}"""',
            code,
            flags=re.DOTALL,
        )

    def _template_literals(self, code):
        """`Hola ${nombre}` → f\"Hola {nombre}\""""
        def reemplazar(m):
            interior = re.sub(r'\$\{([^}]+)\}', r'{\1}', m.group(1))
            interior = interior.replace('"', '\\"')
            return f'f"{interior}"'
        return re.sub(r'`([^`]*)`', reemplazar, code)

    # --- Traduccion linea por linea ---

    def _translate_line(self, line):
        line = self._single_comment(line)
        line = self._else_if(line)
        line = self._else_clause(line)
        line = self._if_stmt(line)
        line = self._while_stmt(line)
        line = self._for_of(line)
        line = self._for_in(line)
        line = self._for_classic(line)
        line = self._function_def(line)
        line = self._arrow_function(line)
        line = self._variable_decl(line)
        line = self._console_log(line)
        line = self._operators(line)
        line = self._keywords(line)
        line = self._remove_trailing_brace(line)
        line = self._remove_semicolon(line)
        return line.strip()

    # --- Reglas individuales ---

    def _single_comment(self, line):
        """// comentario → # comentario"""
        return re.sub(r'//(.*)', r'#\1', line)

    def _else_if(self, line):
        """} else if (cond) { → elif cond:"""
        m = re.match(r'^\}?\s*else\s+if\s*\((.+)\)\s*\{?$', line)
        if m:
            return f'elif {m.group(1).strip()}:'
        return line

    def _else_clause(self, line):
        """} else { → else:"""
        if re.match(r'^\}?\s*else\s*\{?$', line.strip()):
            return 'else:'
        return line

    def _if_stmt(self, line):
        """if (cond) { → if cond:"""
        m = re.match(r'^if\s*\((.+)\)\s*\{?$', line)
        if m:
            return f'if {m.group(1).strip()}:'
        return line

    def _while_stmt(self, line):
        """while (cond) { → while cond:"""
        m = re.match(r'^while\s*\((.+)\)\s*\{?$', line)
        if m:
            return f'while {m.group(1).strip()}:'
        return line

    def _for_of(self, line):
        """for (let x of lista) { → for x in lista:"""
        m = re.match(
            r'^for\s*\(\s*(?:let|const|var)\s+(\w+)\s+of\s+(.+)\)\s*\{?$', line
        )
        if m:
            return f'for {m.group(1)} in {m.group(2).strip()}:'
        return line

    def _for_in(self, line):
        """for (let k in obj) { → for k in obj:"""
        m = re.match(
            r'^for\s*\(\s*(?:let|const|var)\s+(\w+)\s+in\s+(.+)\)\s*\{?$', line
        )
        if m:
            return f'for {m.group(1)} in {m.group(2).strip()}:'
        return line

    def _for_classic(self, line):
        """
        for (let i = 0; i < n; i++) { → for i in range(0, n):
        Soporta: i++, i--, i+=paso, i-=paso y operadores <, <=, >, >=
        """
        m = re.match(
            r'^for\s*\(\s*(?:let|const|var)?\s*(\w+)\s*=\s*(.+?);\s*'
            r'\1\s*([<>]=?)\s*(.+?);\s*\1(.+?)\s*\)\s*\{?$',
            line,
        )
        if not m:
            return line

        var   = m.group(1)
        start = m.group(2).strip()
        op    = m.group(3)
        end   = m.group(4).strip()
        step  = m.group(5).strip()

        paso = self._parse_step(step)

        if op == '<':
            fin = end
        elif op == '<=':
            fin = f'{end} + 1'
        elif op == '>':
            fin = end
        elif op == '>=':
            fin = f'{end} - 1'
        else:
            fin = end

        if paso is None or paso == '1':
            return f'for {var} in range({start}, {fin}):'
        return f'for {var} in range({start}, {fin}, {paso}):'

    def _parse_step(self, expr):
        """Convierte ++, --, +=n, -=n al valor de paso para range()."""
        if expr in ('++', '+= 1', '+=1'):
            return None
        if expr in ('--', '-= 1', '-=1'):
            return '-1'
        m = re.match(r'\+=\s*(.+)', expr)
        if m:
            return m.group(1).strip()
        m = re.match(r'-=\s*(.+)', expr)
        if m:
            return f'-{m.group(1).strip()}'
        return None

    def _function_def(self, line):
        """[async] function nombre(params) { → [async] def nombre(params):"""
        m = re.match(
            r'^(?:(async)\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{?$', line
        )
        if m:
            prefix = 'async ' if m.group(1) else ''
            return f'{prefix}def {m.group(2)}({m.group(3).strip()}):'
        return line

    def _arrow_function(self, line):
        """
        const nombre = (params) => { → def nombre(params):
        const nombre = (params) => expr; → def nombre(params): return expr
        """
        # Con parentesis
        m = re.match(
            r'^(?:const|let|var)\s+(\w+)\s*=\s*(async\s*)?\(([^)]*)\)\s*=>\s*(.*)$',
            line,
        )
        if not m:
            # Sin parentesis (un solo param): const doble = x => ...
            m = re.match(
                r'^(?:const|let|var)\s+(\w+)\s*=\s*(async\s*)?(\w+)\s*=>\s*(.*)$',
                line,
            )
        if m:
            nombre   = m.group(1)
            prefix   = 'async ' if m.group(2) else ''
            params   = m.group(3).strip()
            cuerpo   = m.group(4).strip().rstrip(';').rstrip('{').strip()
            if cuerpo:
                return f'{prefix}def {nombre}({params}):\n    return {cuerpo}'
            return f'{prefix}def {nombre}({params}):'
        return line

    def _variable_decl(self, line):
        """let/const/var nombre = valor → nombre = valor"""
        m = re.match(r'^(?:let|const|var)\s+(\w+)\s*=\s*(.+)$', line)
        if m:
            return f'{m.group(1)} = {m.group(2).strip()}'
        # Sin valor: let x; → x = None
        m = re.match(r'^(?:let|const|var)\s+(\w+)\s*;?$', line)
        if m:
            return f'{m.group(1)} = None'
        return line

    def _console_log(self, line):
        """console.log(...) → print(...)"""
        return re.sub(r'\bconsole\.log\b', 'print', line)

    def _operators(self, line):
        """=== → ==, !== → !=, && → and, || → or, ! → not"""
        line = line.replace('===', '==')
        line = line.replace('!==', '!=')
        line = line.replace('&&', 'and')
        line = line.replace('||', 'or')
        line = re.sub(r'(?<![=!])!(?!=)', 'not ', line)
        return line

    def _keywords(self, line):
        """true→True, false→False, null→None, undefined→None"""
        line = re.sub(r'\btrue\b',      'True',  line)
        line = re.sub(r'\bfalse\b',     'False', line)
        line = re.sub(r'\bnull\b',      'None',  line)
        line = re.sub(r'\bundefined\b', 'None',  line)
        return line

    def _remove_trailing_brace(self, line):
        return re.sub(r'\s*\{$', '', line)

    def _remove_semicolon(self, line):
        return line.rstrip(';')


def build_translator():
    return JSTranslator()
