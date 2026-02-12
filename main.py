# main.py
# Simple Tkinter GUI to run the PLY lexer.

import tkinter as tk
from tkinter import ttk

from lexer import build_lexer


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

        output_frame = ttk.Frame(self)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        output_label = ttk.Label(output_frame, text="Tokens:")
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
        if errors:
            for char, line, pos in errors:
                self.error_text.insert(
                    tk.END,
                    f"Caracter inesperado '{char}' en linea {line}, posicion {pos}.\n",
                )
        self.error_text.configure(state="disabled")

    def analyze(self):
        for item in self.token_table.get_children():
            self.token_table.delete(item)
        self._set_errors([])

        data = self.input_text.get("1.0", tk.END)
        lexer = build_lexer()
        lexer.input(data)

        for token in lexer:
            self.token_table.insert(
                "",
                tk.END,
                values=(token.type, token.value, token.lineno, token.lexpos),
            )

        if lexer.errors:
            self._set_errors(lexer.errors)


if __name__ == "__main__":
    app = LexerApp()
    app.mainloop()
