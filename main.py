# main.py
# Interfaz grafica del compilador con todas las fases.

import tkinter as tk
from tkinter import ttk
import os

from lexer import build_lexer
from parser import build_parser
from semantic import build_semantic_analyzer
from intermediate import build_intermediate_generator
from translator import build_translator
from executor import build_executor


class CompilerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compilador - Analizador Lexico, Sintactico, Semantico, Codigo Intermedio y Traductor")
        self.geometry("1100x750")

        self._last_parse_result = None
        self._last_semantic_errors = []
        self._last_symbol_table = []
        self._last_intermediate_code = []

        self._build_ui()

    def _build_ui(self):
        # --- Titulo ---
        header = ttk.Label(
            self,
            text="Compilador",
            font=("Helvetica", 20, "bold"),
        )
        header.pack(pady=8)

        # --- Entrada ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.BOTH, expand=False, padx=10)

        input_label = ttk.Label(top_frame, text="Codigo fuente (JavaScript / lenguaje del compilador):")
        input_label.pack(anchor="w")

        self.input_text = tk.Text(top_frame, height=10, wrap="none", font=("Courier", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # --- Botones ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=8)

        analyze_btn = ttk.Button(button_frame, text="Analizar", command=self.analyze)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 6))

        symbol_btn = ttk.Button(button_frame, text="Tabla de Simbolos", command=self.show_symbol_table)
        symbol_btn.pack(side=tk.LEFT, padx=6)

        intermediate_btn = ttk.Button(button_frame, text="Codigo Intermedio", command=self.show_intermediate_code)
        intermediate_btn.pack(side=tk.LEFT, padx=6)

        translate_btn = ttk.Button(
            button_frame, text="Traducir JS \u2192 EspanolScript", command=self.translate_code
        )
        translate_btn.pack(side=tk.LEFT, padx=6)

        execute_btn = ttk.Button(button_frame, text="Ejecutar Codigo", command=self.execute_code)
        execute_btn.pack(side=tk.LEFT, padx=6)

        clear_btn = ttk.Button(button_frame, text="Limpiar", command=self.clear_all)
        clear_btn.pack(side=tk.RIGHT)

        # --- Tabla de tokens ---
        output_frame = ttk.Frame(self)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 4))

        output_label = ttk.Label(output_frame, text="Tokens lexicos:")
        output_label.pack(anchor="w")

        columns = ("type", "value", "line", "pos")
        self.token_table = ttk.Treeview(
            output_frame,
            columns=columns,
            show="headings",
            height=8,
        )
        self.token_table.heading("type", text="Tipo")
        self.token_table.heading("value", text="Valor")
        self.token_table.heading("line", text="Linea")
        self.token_table.heading("pos", text="Posicion")
        self.token_table.column("type", width=140)
        self.token_table.column("value", width=340)
        self.token_table.column("line", width=80, anchor="center")
        self.token_table.column("pos", width=80, anchor="center")

        token_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.token_table.yview)
        self.token_table.configure(yscrollcommand=token_scroll.set)
        self.token_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        token_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Errores ---
        error_frame = ttk.Frame(self)
        error_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 8))

        error_label = ttk.Label(error_frame, text="Errores:")
        error_label.pack(anchor="w")

        self.error_text = tk.Text(error_frame, height=4, wrap="word", font=("Courier", 9))
        self.error_text.pack(fill=tk.BOTH, expand=False)
        self.error_text.configure(state="disabled")

    # --- Acciones ---

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self._clear_tokens()
        self._set_errors([])
        self._last_parse_result = None
        self._last_semantic_errors = []
        self._last_symbol_table = []
        self._last_intermediate_code = []

    def _set_errors(self, errors):
        self.error_text.configure(state="normal")
        self.error_text.delete("1.0", tk.END)
        for error in errors:
            self.error_text.insert(tk.END, f"{error}\n")
        self.error_text.configure(state="disabled")

    def _clear_tokens(self):
        for item in self.token_table.get_children():
            self.token_table.delete(item)

    def _build_error_messages(self, parse_result, errores_semanticos=None):
        errors = []

        for char, line, pos in parse_result["errores_lexicos"]:
            errors.append(
                f"[Lexico] Caracter inesperado '{char}' en linea {line}, posicion {pos}."
            )

        for error in parse_result["errores_sintacticos"]:
            errors.append(
                f"[Sintactico] {error['mensaje']} en linea {error['linea']}, posicion {error['posicion']}."
            )

        for error in (errores_semanticos or []):
            errors.append(f"[Semantico] {error['mensaje']}.")

        if not errors:
            errors.append("Analisis completado sin errores.")

        return errors

    def analyze(self):
        """Ejecuta analisis lexico, sintactico, semantico, tabla de simbolos y codigo intermedio."""
        self._clear_tokens()
        self._set_errors([])

        data = self.input_text.get("1.0", tk.END)

        # Parser (incluye lexer internamente)
        parser = build_parser()
        parse_result = parser.parse(data)
        self._last_parse_result = parse_result

        # Semantico y tabla de simbolos
        errores_semanticos = []
        self._last_symbol_table = []
        self._last_intermediate_code = []

        if parse_result["arbol"] is not None and not parse_result["errores_sintacticos"]:
            analyzer = build_semantic_analyzer()
            errores_semanticos = analyzer.analyze(parse_result["arbol"])
            self._last_semantic_errors = errores_semanticos

            # Extraer tabla de simbolos del analizador semantico
            self._last_symbol_table = analyzer.all_symbols

            # Generar codigo intermedio
            gen = build_intermediate_generator()
            self._last_intermediate_code = gen.generate(parse_result["arbol"])

        # Poblar tabla de tokens
        lexer = build_lexer()
        lexer.input(data)
        for token in lexer:
            self.token_table.insert(
                "",
                tk.END,
                values=(token.type, token.value, token.lineno, token.lexpos),
            )

        self._set_errors(self._build_error_messages(parse_result, errores_semanticos))

    def show_symbol_table(self):
        """Muestra la tabla de simbolos en una ventana emergente."""
        if not self._last_symbol_table:
            self._show_info_window(
                "Tabla de Simbolos",
                "No hay simbolos. Ejecute el analisis primero con el boton 'Analizar'."
            )
            return

        win = tk.Toplevel(self)
        win.title("Tabla de Simbolos")
        win.geometry("500x400")

        ttk.Label(
            win,
            text="Tabla de Simbolos",
            font=("Helvetica", 14, "bold"),
        ).pack(pady=8, anchor="w", padx=12)

        frame = ttk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 4))

        columns = ("nombre", "tipo", "scope")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        tree.heading("nombre", text="Nombre")
        tree.heading("tipo", text="Tipo")
        tree.heading("scope", text="Alcance")
        tree.column("nombre", width=160)
        tree.column("tipo", width=120)
        tree.column("scope", width=160)

        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        for sym in self._last_symbol_table:
            tree.insert("", tk.END, values=(sym["nombre"], sym["tipo"], sym["scope"]))

        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=8)

    def show_intermediate_code(self):
        """Muestra el codigo intermedio en una ventana emergente."""
        if not self._last_intermediate_code:
            self._show_info_window(
                "Codigo Intermedio",
                "No hay codigo intermedio. Ejecute el analisis primero con el boton 'Analizar'."
            )
            return

        code_text = "\n".join(self._last_intermediate_code)
        self._open_code_window("Codigo Intermedio (Three-Address Code)", code_text)

    def translate_code(self):
        """Traduce el codigo JavaScript de la entrada a EspanolScript."""
        data = self.input_text.get("1.0", tk.END).strip()
        if not data:
            return

        translator = build_translator()
        result = translator.translate(data)
        self._open_code_window("Resultado de traduccion — EspañolScript", result)

    def execute_code(self):
        """Ejecuta el codigo intermedio convirtiendolo a JavaScript."""
        if not self._last_intermediate_code:
            self._show_info_window(
                "Ejecutar Codigo",
                "No hay codigo intermedio para ejecutar. Ejecute el analisis primero con el boton 'Analizar'."
            )
            return

        executor = build_executor()
        result = executor.execute_intermediate_code(
            self._last_intermediate_code,
            output_dir=os.path.dirname(os.path.abspath(__file__))
        )

        self._show_execution_result(result)

    def _open_code_window(self, title, code):
        """Abre una ventana emergente con codigo de solo lectura."""
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("720x520")

        ttk.Label(
            win,
            text=title,
            font=("Helvetica", 12, "bold"),
        ).pack(pady=8, anchor="w", padx=12)

        frame = ttk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 4))

        scroll_y = ttk.Scrollbar(frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = ttk.Scrollbar(frame, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        text = tk.Text(
            frame,
            wrap="none",
            font=("Courier", 11),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )
        text.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=text.yview)
        scroll_x.config(command=text.xview)

        text.insert("1.0", code)
        text.configure(state="disabled")

        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=8)

    def _show_info_window(self, title, message):
        """Muestra una ventana con un mensaje informativo."""
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("400x150")
        ttk.Label(win, text=message, wraplength=360, font=("Helvetica", 11)).pack(pady=30, padx=20)
        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=8)

    def _show_execution_result(self, result):
        """Muestra el resultado de la ejecucion de codigo en una ventana emergente."""
        win = tk.Toplevel(self)
        win.title("Resultado de Ejecucion")
        win.geometry("800x600")

        ttk.Label(
            win,
            text="Resultado de Ejecucion",
            font=("Helvetica", 14, "bold"),
        ).pack(pady=8, anchor="w", padx=12)

        # Informacion del archivo generado
        if result['js_file']:
            ttk.Label(
                win,
                text=f"Archivo JavaScript generado: {os.path.basename(result['js_file'])}",
                font=("Helvetica", 10),
            ).pack(anchor="w", padx=12)

        # Estado de la ejecucion
        status_text = "✓ Ejecutado exitosamente" if result['success'] else "✗ Error en la ejecución"

        status_label = ttk.Label(
            win,
            text=status_text,
            font=("Helvetica", 11, "bold"),
        )
        status_label.pack(anchor="w", padx=12, pady=(5, 0))

        # Notebook para separar output y errores
        notebook = ttk.Notebook(win)
        notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Tab de salida
        output_frame = ttk.Frame(notebook)
        notebook.add(output_frame, text="Salida del Programa")

        output_scroll_y = ttk.Scrollbar(output_frame)
        output_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        output_text = tk.Text(
            output_frame,
            wrap="word",
            font=("Courier", 10),
            yscrollcommand=output_scroll_y.set,
        )
        output_text.pack(fill=tk.BOTH, expand=True)
        output_scroll_y.config(command=output_text.yview)

        output_content = result['output'] if result['output'] else "(No hay salida)"
        output_text.insert("1.0", output_content)
        output_text.configure(state="disabled")

        # Tab de errores (solo si hay errores)
        if result['error']:
            error_frame = ttk.Frame(notebook)
            notebook.add(error_frame, text="Errores")

            error_scroll_y = ttk.Scrollbar(error_frame)
            error_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

            error_text = tk.Text(
                error_frame,
                wrap="word",
                font=("Courier", 10),
                yscrollcommand=error_scroll_y.set,
                fg="red",
            )
            error_text.pack(fill=tk.BOTH, expand=True)
            error_scroll_y.config(command=error_text.yview)

            error_text.insert("1.0", result['error'])
            error_text.configure(state="disabled")

        # Botones
        button_frame = ttk.Frame(win)
        button_frame.pack(pady=8)

        ttk.Button(button_frame, text="Cerrar", command=win.destroy).pack(side=tk.RIGHT, padx=5)

        if result['js_file'] and os.path.exists(result['js_file']):
            def open_js_file():
                try:
                    with open(result['js_file'], 'r', encoding='utf-8') as f:
                        js_content = f.read()
                    self._open_code_window("Codigo JavaScript Generado", js_content)
                except Exception as e:
                    self._show_info_window("Error", f"No se pudo leer el archivo: {str(e)}")

            ttk.Button(button_frame, text="Ver JS Generado", command=open_js_file).pack(side=tk.RIGHT, padx=5)


if __name__ == "__main__":
    app = CompilerApp()
    app.mainloop()
