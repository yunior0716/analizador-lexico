# Analizador lexico y sintactico

El analizador lexico (lexer) toma el texto de entrada y lo divide en tokens.
Un token es una pieza con tipo (por ejemplo, `SI`, `ID`, `NUMERO`) y valor.
Con PLY, cada regla (regex) identifica una categoria de token y el lexer
recorre el texto de izquierda a derecha generando la lista de tokens.

Ademas, el analizador sintactico (parser) valida la estructura del codigo
usando la secuencia de tokens y reporta errores de sintaxis.

### Estructura del proyecto

- `main.py`: interfaz principal (Tkinter) y punto de entrada de la aplicacion.
- `lexer.py`: reglas del analizador lexico.
- `parser.py`: reglas del analizador sintactico.

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

# Analizador semantico:

recorre el AST y verifica que el programa tenga sentido.

# Verificaciones que realiza:

1. Variable no declarada → usar una variable que no fue declarada antes
2. Variable re-declarada → declarar la misma variable dos veces en el mismo bloque
3. Tipos incompatibles → asignar un valor del tipo incorrecto a una variable

### Ejemplo para probar analizador semantico

```
int x = 10;
float y = 3.14;
bool activo = true;
string nombre = "Juan";

int x = 5;

int edad = "veinte";

if (activo == true) {
    int resultado = x + y;
    z = 99;
}
```
