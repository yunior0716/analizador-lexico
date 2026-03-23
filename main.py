# main.py
# Simple Tkinter GUI to run the PLY lexer.

import tkinter as tk
from tkinter import ttk

from lexer import build_lexer
from parser import build_parser
from semantic import build_semantic_analyzer
from translator import build_translator


class LexerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Lexico")
        self.geometry("900x600")

        self._build_ui()

    def _build_ui(self):
        header = ttk.Label(
            self,
            text="Analizador Lexico",
            font=("Helvetica", 18, "bold"),
        )
        header.pack(pady=10)

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.BOTH, expand=False, padx=10)

        input_label = ttk.Label(top_frame, text="Entrada:")
        input_label.pack(anchor="w")

        self.input_text = tk.Text(top_frame, height=10, wrap="none")
        self.input_text.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=8)

        analyze_btn = ttk.Button(button_frame, text="Analizar", command=self.analyze)
        analyze_btn.pack(side=tk.LEFT)

        clear_btn = ttk.Button(button_frame, text="Limpiar", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=8)

        translate_btn = ttk.Button(
            button_frame, text="Traducir JS → Py", command=self.translate_code
        )
        translate_btn.pack(side=tk.LEFT)

        output_frame = ttk.Frame(self)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        output_label = ttk.Label(output_frame, text="Tokens lexicos:")
        output_label.pack(anchor="w")

        columns = ("type", "value", "line", "pos")
        self.token_table = ttk.Treeview(
            output_frame,
            columns=columns,
            show="headings",
            height=10,
        )
        self.token_table.heading("type", text="Tipo")
        self.token_table.heading("value", text="Valor")
        self.token_table.heading("line", text="Linea")
        self.token_table.heading("pos", text="Posicion")
        self.token_table.column("type", width=140)
        self.token_table.column("value", width=340)
        self.token_table.column("line", width=80, anchor="center")
        self.token_table.column("pos", width=80, anchor="center")
        self.token_table.pack(fill=tk.BOTH, expand=True)

        error_label = ttk.Label(output_frame, text="Errores:")
        error_label.pack(anchor="w", pady=(10, 0))

        self.error_text = tk.Text(output_frame, height=4, wrap="word")
        self.error_text.pack(fill=tk.BOTH, expand=False)
        self.error_text.configure(state="disabled")

    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        for item in self.token_table.get_children():
            self.token_table.delete(item)
        self._set_errors([])

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
        self._clear_tokens()
        self._set_errors([])

        data = self.input_text.get("1.0", tk.END)

        parser = build_parser()
        parse_result = parser.parse(data)

        # Ejecutar el analizador semantico solo si el AST fue construido
        # (es decir, no hubo errores sintacticos que impidieran construirlo)
        errores_semanticos = []
        if parse_result["arbol"] is not None and not parse_result["errores_sintacticos"]:
            analyzer = build_semantic_analyzer()
            errores_semanticos = analyzer.analyze(parse_result["arbol"])

        lexer = build_lexer()
        lexer.input(data)

        for token in lexer:
            self.token_table.insert(
                "",
                tk.END,
                values=(token.type, token.value, token.lineno, token.lexpos),
            )

        self._set_errors(self._build_error_messages(parse_result, errores_semanticos))

    def translate_code(self):
        """Traduce el codigo JavaScript de la entrada a Python."""
        data = self.input_text.get("1.0", tk.END).strip()
        if not data:
            return

        translator = build_translator()
        python_code = translator.translate(data)
        self._open_translator_window(python_code)

    def _open_translator_window(self, python_code: str):
        """
        Abre una ventana emergente con el código Python traducido.
        El contenido es de solo lectura y tiene barras de desplazamiento.
        """
        win = tk.Toplevel(self)
        win.title("Resultado de traduccion — Python")
        win.geometry("720x520")

        ttk.Label(
            win,
            text="Código Python traducido:",
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

        text.insert("1.0", python_code)
        text.configure(state="disabled")

        ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=8)


if __name__ == "__main__":
    app = LexerApp()
    app.mainloop()
