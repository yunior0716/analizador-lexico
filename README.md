# Analizador lexico

El analizador lexico (lexer) toma el texto de entrada y lo divide en tokens.
Un token es una pieza con tipo (por ejemplo, `SI`, `ID`, `NUMERO`) y valor.
Con PLY, cada regla (regex) identifica una categoria de token y el lexer
recorre el texto de izquierda a derecha generando la lista de tokens.

### Que detecta

- Palabras reservadas: `if`, `else`, `while`, `for`, `return`, `int`, `float`,
  `string`, `bool`, `true`, `false`.
- Identificadores: nombres de variables o funciones.
- Numeros: enteros y decimales.
- Cadenas: entre comillas dobles (soporta escapes simples).
- Operadores y simbolos: `+ - * / = == != < <= > >= ( ) { } ; ,`.
- Comentarios: `//` en una linea y `/* ... */` multilinea.

### Significado de tokens

- `ID`: identificador (nombres de variables, funciones, etc.).
- `NUMERO`: numero entero o decimal.
- `LITERAL_CADENA`: cadena de texto entre comillas dobles.
- `MAS`: operador suma `+`.
- `MENOS`: operador resta `-`.
- `POR`: operador multiplicacion `*`.
- `DIVIDIR`: operador division `/`.
- `ASIGNAR`: asignacion `=`.
- `IGUAL`: igualdad `==`.
- `DISTINTO`: distinto `!=`.
- `MENOR`: menor que `<`.
- `MENOR_IGUAL`: menor o igual `<=`.
- `MAYOR`: mayor que `>`.
- `MAYOR_IGUAL`: mayor o igual `>=`.
- `PAREN_IZQ`: parentesis izquierdo `(`.
- `PAREN_DER`: parentesis derecho `)`.
- `LLAVE_IZQ`: llave izquierda `{`.
- `LLAVE_DER`: llave derecha `}`.
- `PUNTO_Y_COMA`: punto y coma `;`.
- `COMA`: coma `,`.

### Palabras reservadas

- `SI`, `SINO`, `MIENTRAS`, `PARA`, `RETORNAR`
- `ENTERO`, `FLOTANTE`, `CADENA`, `BOOLEANO`
- `VERDADERO`, `FALSO`

### Ejemplos para probar

Ejemplo 1: control de flujo basico

```
int x = 10;
if (x >= 5) {
	x = x + 1;
}
```

Ejemplo 2: bucle y comentario

```
// contador
int i = 0;
while (i < 3) {
	i = i + 1;
}
```

Ejemplo 3: tipos, string y booleanos

```
string name = "Ada";
bool ok = true;
```

Ejemplo 4: error lexico

```
int $x = 1;
```

El simbolo `$` no esta definido como token y se reporta como error.
