# Compilador — Analizador lexico, sintactico, semantico y traductor JS → Python

Este proyecto implementa las tres primeras fases de un compilador mas un traductor de codigo:

1. **Lexico** — divide el texto en tokens.
2. **Sintactico** — verifica que la estructura del codigo sea valida y construye el AST.
3. **Semantico** — verifica que el significado del programa sea correcto (tipos, declaraciones).
4. **Traductor** — convierte codigo JavaScript a Python.

---

## Estructura del proyecto

| Archivo | Descripcion |
|---|---|
| `main.py` | Interfaz grafica (Tkinter) y punto de entrada de la aplicacion |
| `lexer.py` | Reglas del analizador lexico |
| `parser.py` | Reglas del analizador sintactico y construccion del AST |
| `semantic.py` | Analizador semantico: tabla de simbolos y verificacion de tipos |
| `translator.py` | Traductor de JavaScript a Python |

---

## Analizador lexico

El lexer toma el texto de entrada y lo divide en tokens. Con PLY, cada regla (regex)
identifica una categoria de token y el lexer recorre el texto de izquierda a derecha.

### Tokens reconocidos

| Token | Descripcion | Simbolo |
|---|---|---|
| `ID` | Identificador (nombre de variable, funcion, etc.) | `miVariable` |
| `NUMERO` | Numero entero o decimal | `42`, `3.14` |
| `LITERAL_CADENA` | Cadena entre comillas dobles | `"hola"` |
| `MAS` | Suma | `+` |
| `MENOS` | Resta | `-` |
| `POR` | Multiplicacion | `*` |
| `DIVIDIR` | Division | `/` |
| `ASIGNAR` | Asignacion | `=` |
| `IGUAL` | Igualdad | `==` |
| `DISTINTO` | Distinto de | `!=` |
| `MENOR` | Menor que | `<` |
| `MENOR_IGUAL` | Menor o igual | `<=` |
| `MAYOR` | Mayor que | `>` |
| `MAYOR_IGUAL` | Mayor o igual | `>=` |
| `PAREN_IZQ` | Parentesis izquierdo | `(` |
| `PAREN_DER` | Parentesis derecho | `)` |
| `LLAVE_IZQ` | Llave izquierda | `{` |
| `LLAVE_DER` | Llave derecha | `}` |
| `PUNTO_Y_COMA` | Punto y coma | `;` |
| `COMA` | Coma | `,` |

### Palabras reservadas

| Token | Palabra clave |
|---|---|
| `SI` | `if` |
| `SINO` | `else` |
| `MIENTRAS` | `while` |
| `PARA` | `for` |
| `RETORNAR` | `return` |
| `ENTERO` | `int` |
| `FLOTANTE` | `float` |
| `CADENA` | `string` |
| `BOOLEANO` | `bool` |
| `VERDADERO` | `true` |
| `FALSO` | `false` |

### Ejemplos para probar el lexico y el sintactico

**Ejemplo 1 — Control de flujo basico**
```
int x = 10;
if (x >= 5) {
    x = x + 1;
}
```

**Ejemplo 2 — Bucle y comentario**
```
// contador
int i = 0;
while (i < 3) {
    i = i + 1;
}
```

**Ejemplo 3 — Tipos string y booleano**
```
string name = "Ada";
bool ok = true;
```

**Ejemplo 4 — Error lexico**
```
int $x = 1;
```
El simbolo `$` no esta definido como token y se reporta como error lexico.

---

## Analizador sintactico

El parser valida que la secuencia de tokens siga la gramatica del lenguaje y construye
un AST (arbol de sintaxis abstracta) como diccionarios Python anidados.

Estructuras soportadas: declaraciones, asignaciones, `if/else`, `while`, `for`, `return`,
bloques `{ }` y expresiones aritmeticas/logicas.

---

## Analizador semantico

Recorre el AST y verifica que el programa tenga sentido logico. Usa una
**tabla de simbolos** (pila de diccionarios) que recuerda que variables existen
y de que tipo son en cada bloque `{ }`.

### Verificaciones que realiza

| # | Verificacion | Ejemplo de error |
|---|---|---|
| 1 | **Variable no declarada** | Usar `x` sin haberla declarado antes |
| 2 | **Variable re-declarada** | Declarar `int x;` dos veces en el mismo bloque |
| 3 | **Tipos incompatibles** | `int x = "hola";` o `bool y = 3.14;` |

### Ejemplos para probar el semantico

**Sin errores:**
```
int x = 5;
float y = x;
int z = x + 2;
```

**Variable no declarada:**
```
x = 10;
```
> `[Semantico] Variable 'x' no ha sido declarada.`

**Variable re-declarada:**
```
int x = 1;
int x = 2;
```
> `[Semantico] Variable 'x' ya fue declarada en este bloque.`

**Tipo incompatible:**
```
int x = "hola";
```
> `[Semantico] Tipo incompatible para 'x': se esperaba 'int', se encontro 'string'.`

**Ejemplo completo con varios errores:**
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

Errores esperados:
- `[Semantico] Variable 'x' ya fue declarada en este bloque.`
- `[Semantico] Tipo incompatible para 'edad': se esperaba 'int', se encontro 'string'.`
- `[Semantico] Tipo incompatible para 'resultado': se esperaba 'int', se encontro 'float'.`
- `[Semantico] Variable 'z' no ha sido declarada.`

---

## Traductor JavaScript → Python

El boton **"Traducir JS → Py"** toma el codigo del area de entrada, lo convierte a
Python y muestra el resultado en una ventana nueva.

El traductor trabaja en dos pasos:
1. Transformaciones multi-linea (comentarios de bloque y template literals).
2. Recorre linea por linea aplicando reglas y gestionando la indentacion segun las llaves `{ }`.

### Construcciones soportadas

#### Variables

| JavaScript | Python |
|---|---|
| `let x = 5;` | `x = 5` |
| `const PI = 3.14;` | `PI = 3.14` |
| `var name;` | `name = None` |

#### Funciones

| JavaScript | Python |
|---|---|
| `function sum(a, b) {` | `def sum(a, b):` |
| `async function fetch() {` | `async def fetch():` |
| `const f = (x) => x * 2;` | `def f(x):` + `return x * 2` |
| `const f = (a, b) => {` | `def f(a, b):` |

#### Condicionales

| JavaScript | Python |
|---|---|
| `if (x > 0) {` | `if x > 0:` |
| `} else if (x < 0) {` | `elif x < 0:` |
| `} else {` | `else:` |

#### Bucles

| JavaScript | Python |
|---|---|
| `while (cond) {` | `while cond:` |
| `for (let i = 0; i < n; i++) {` | `for i in range(0, n):` |
| `for (let i = 0; i <= n; i++) {` | `for i in range(0, n + 1):` |
| `for (let i = 0; i < 20; i += 2) {` | `for i in range(0, 20, 2):` |
| `for (let i = 10; i > 0; i--) {` | `for i in range(10, 0, -1):` |
| `for (let x of lista) {` | `for x in lista:` |
| `for (let k in obj) {` | `for k in obj:` |

#### Impresion

| JavaScript | Python |
|---|---|
| `console.log(msg);` | `print(msg)` |
| `console.log("resultado:", x);` | `print("resultado:", x)` |

#### Comentarios

| JavaScript | Python |
|---|---|
| `// texto` | `# texto` |
| `/* bloque */` | `""" bloque """` |

#### Operadores

| JavaScript | Python |
|---|---|
| `===` | `==` |
| `!==` | `!=` |
| `&&` | `and` |
| `\|\|` | `or` |
| `!expr` | `not expr` |

#### Literales

| JavaScript | Python |
|---|---|
| `true` | `True` |
| `false` | `False` |
| `null` | `None` |
| `undefined` | `None` |

#### Template literals

| JavaScript | Python |
|---|---|
| `` `Hola ${nombre}` `` | `f"Hola {nombre}"` |
| `` `El resultado es ${a + b}` `` | `f"El resultado es {a + b}"` |

### Ejemplos para probar el traductor

Pega el codigo JavaScript en el area de entrada y presiona **"Traducir JS → Py"**.

---

**Ejemplo 1 — Variables y funcion basica**

```javascript
function sumar(a, b) {
    let resultado = a + b;
    return resultado;
}

const saludar = (nombre) => {
    console.log(`Hola ${nombre}!`);
}
```

Resultado esperado:
```python
def sumar(a, b):
    resultado = a + b
    return resultado

def saludar(nombre):
    print(f"Hola {nombre}!")
```

---

**Ejemplo 2 — Bucle for y condicional**

```javascript
for (let i = 0; i < 5; i++) {
    if (i === 2) {
        console.log("es dos");
    } else {
        console.log(i);
    }
}
```

Resultado esperado:
```python
for i in range(0, 5):
    if i == 2:
        print("es dos")
    else:
        print(i)
```

---

**Ejemplo 3 — For...of y operadores logicos**

```javascript
const lista = [1, 2, 3];
for (let num of lista) {
    if (num > 1 && num !== 3) {
        console.log(num);
    }
}
```

Resultado esperado:
```python
lista = [1, 2, 3]
for num in lista:
    if num > 1 and num != 3:
        print(num)
```

---

**Ejemplo 4 — While y template literal**

```javascript
let contador = 0;
while (contador < 3) {
    console.log(`Vuelta numero ${contador}`);
    contador = contador + 1;
}
```

Resultado esperado:
```python
contador = 0
while contador < 3:
    print(f"Vuelta numero {contador}")
    contador = contador + 1
```

---

**Ejemplo 5 — Operadores y literales**

```javascript
let x = null;
let y = undefined;
let ok = true;

if (!ok || x === null) {
    console.log("condicion cumplida");
}
```

Resultado esperado:
```python
x = None
y = None
ok = True

if not ok or x == None:
    print("condicion cumplida")
```
