# translator.py
# Traduce codigo JavaScript a EspañolScript (lenguaje natural en español).
import re


class JSTranslator:
    """Traduce codigo JavaScript basico a EspañolScript (español natural)."""

    def translate(self, code):
        """Recibe codigo JS como string y devuelve el equivalente en EspañolScript."""
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

            # Llave de cierre sola -> reduce indent
            if re.match(r'^\}[;,]?$', stripped):
                indent = max(0, indent - 1)
                result.append('    ' * indent + 'fin')
                continue

            # } else ... -> reduce indent antes de traducir
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
        """/* texto */ -> --- texto ---"""
        return re.sub(
            r'/\*(.*?)\*/',
            lambda m: f'--- {m.group(1).strip()} ---',
            code,
            flags=re.DOTALL,
        )

    def _template_literals(self, code):
        """`Hola ${nombre}` -> "Hola {nombre}" """
        def reemplazar(m):
            interior = re.sub(r'\$\{([^}]+)\}', r'{\1}', m.group(1))
            return f'"{interior}"'
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
        line = self._return_stmt(line)
        line = self._remove_trailing_brace(line)
        line = self._remove_semicolon(line)
        return line.strip()

    # --- Reglas individuales ---

    def _single_comment(self, line):
        """// comentario -> ** comentario"""
        return re.sub(r'//(.*)', r'** \1', line)

    def _else_if(self, line):
        """} else if (cond) { -> sino si (cond) entonces"""
        m = re.match(r'^\}?\s*else\s+if\s*\((.+)\)\s*\{?$', line)
        if m:
            cond = self._translate_condition(m.group(1).strip())
            return f'sino si ({cond}) entonces'
        return line

    def _else_clause(self, line):
        """} else { -> sino"""
        if re.match(r'^\}?\s*else\s*\{?$', line.strip()):
            return 'sino'
        return line

    def _if_stmt(self, line):
        """if (cond) { -> si (cond) entonces"""
        m = re.match(r'^if\s*\((.+)\)\s*\{?$', line)
        if m:
            cond = self._translate_condition(m.group(1).strip())
            return f'si ({cond}) entonces'
        return line

    def _while_stmt(self, line):
        """while (cond) { -> mientras (cond) hacer"""
        m = re.match(r'^while\s*\((.+)\)\s*\{?$', line)
        if m:
            cond = self._translate_condition(m.group(1).strip())
            return f'mientras ({cond}) hacer'
        return line

    def _for_of(self, line):
        """for (let x of lista) { -> para cada x en lista hacer"""
        m = re.match(
            r'^for\s*\(\s*(?:let|const|var)\s+(\w+)\s+of\s+(.+)\)\s*\{?$', line
        )
        if m:
            return f'para cada {m.group(1)} en {m.group(2).strip()} hacer'
        return line

    def _for_in(self, line):
        """for (let k in obj) { -> para cada k en obj hacer"""
        m = re.match(
            r'^for\s*\(\s*(?:let|const|var)\s+(\w+)\s+in\s+(.+)\)\s*\{?$', line
        )
        if m:
            return f'para cada {m.group(1)} en {m.group(2).strip()} hacer'
        return line

    def _for_classic(self, line):
        """
        for (let i = 0; i < n; i++) { -> para i desde 0 hasta n hacer
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

        if op in ('<', '<='):
            if paso is None or paso == '1':
                return f'para {var} desde {start} hasta {end} hacer'
            return f'para {var} desde {start} hasta {end} con paso {paso} hacer'
        elif op in ('>', '>='):
            if paso == '-1' or paso is None:
                return f'para {var} desde {start} hasta {end} hacer'
            return f'para {var} desde {start} hasta {end} con paso {paso} hacer'

        return f'para {var} desde {start} hasta {end} hacer'

    def _parse_step(self, expr):
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
        """[async] function nombre(params) { -> funcion nombre(params)"""
        m = re.match(
            r'^(?:(async)\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{?$', line
        )
        if m:
            prefix = 'asincrona ' if m.group(1) else ''
            return f'{prefix}funcion {m.group(2)}({m.group(3).strip()})'
        return line

    def _arrow_function(self, line):
        """
        const nombre = (params) => { -> funcion nombre(params)
        const nombre = (params) => expr; -> funcion nombre(params) devolver expr
        """
        # Con parentesis
        m = re.match(
            r'^(?:const|let|var)\s+(\w+)\s*=\s*(async\s*)?\(([^)]*)\)\s*=>\s*(.*)$',
            line,
        )
        if not m:
            m = re.match(
                r'^(?:const|let|var)\s+(\w+)\s*=\s*(async\s*)?(\w+)\s*=>\s*(.*)$',
                line,
            )
        if m:
            nombre   = m.group(1)
            prefix   = 'asincrona ' if m.group(2) else ''
            params   = m.group(3).strip()
            cuerpo   = m.group(4).strip().rstrip(';').rstrip('{').strip()
            if cuerpo:
                cuerpo = self._translate_expr_keywords(cuerpo)
                return f'{prefix}funcion {nombre}({params})\n    devolver {cuerpo}'
            return f'{prefix}funcion {nombre}({params})'
        return line

    def _variable_decl(self, line):
        """let/const/var nombre = valor -> variable nombre = valor"""
        m = re.match(r'^(?:let|const|var)\s+(\w+)\s*=\s*(.+)$', line)
        if m:
            valor = self._translate_expr_keywords(m.group(2).strip())
            return f'variable {m.group(1)} = {valor}'
        m = re.match(r'^(?:let|const|var)\s+(\w+)\s*;?$', line)
        if m:
            return f'variable {m.group(1)} = nulo'
        return line

    def _console_log(self, line):
        """console.log(...) -> mostrar(...)"""
        return re.sub(r'\bconsole\.log\b', 'mostrar', line)

    def _return_stmt(self, line):
        """return expr -> devolver expr"""
        m = re.match(r'^return\b\s*(.*)', line)
        if m:
            expr = m.group(1).strip().rstrip(';')
            if expr:
                return f'devolver {expr}'
            return 'devolver'
        return line

    def _operators(self, line):
        """=== -> ==, !== -> !=, && -> y, || -> o, ! -> no"""
        line = line.replace('===', '==')
        line = line.replace('!==', '!=')
        line = line.replace('&&', ' y ')
        line = line.replace('||', ' o ')
        line = re.sub(r'(?<![=!])!(?!=)', 'no ', line)
        return line

    def _keywords(self, line):
        """true->verdadero, false->falso, null->nulo, undefined->nulo"""
        line = re.sub(r'\btrue\b',      'verdadero', line)
        line = re.sub(r'\bfalse\b',     'falso',     line)
        line = re.sub(r'\bnull\b',      'nulo',      line)
        line = re.sub(r'\bundefined\b', 'nulo',      line)
        return line

    def _translate_condition(self, cond):
        """Traduce operadores y keywords dentro de condiciones."""
        cond = cond.replace('===', '==')
        cond = cond.replace('!==', '!=')
        cond = cond.replace('&&', ' y ')
        cond = cond.replace('||', ' o ')
        cond = re.sub(r'(?<![=!])!(?!=)', 'no ', cond)
        cond = re.sub(r'\btrue\b',      'verdadero', cond)
        cond = re.sub(r'\bfalse\b',     'falso',     cond)
        cond = re.sub(r'\bnull\b',      'nulo',      cond)
        cond = re.sub(r'\bundefined\b', 'nulo',      cond)
        return cond

    def _translate_expr_keywords(self, expr):
        """Traduce keywords dentro de expresiones."""
        expr = re.sub(r'\btrue\b',      'verdadero', expr)
        expr = re.sub(r'\bfalse\b',     'falso',     expr)
        expr = re.sub(r'\bnull\b',      'nulo',      expr)
        expr = re.sub(r'\bundefined\b', 'nulo',      expr)
        return expr

    def _remove_trailing_brace(self, line):
        return re.sub(r'\s*\{$', '', line)

    def _remove_semicolon(self, line):
        return line.rstrip(';')


def build_translator():
    return JSTranslator()
