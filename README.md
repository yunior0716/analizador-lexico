# Compilador Completo — JavaScript a EspanolScript

Este proyecto implementa un compilador completo con todas las fases clasicas, incluyendo un traductor de JavaScript a **EspanolScript** (un lenguaje de programacion basado en espanol natural, facil de leer y entender).

---

## Fases del compilador

| #   | Fase                      | Archivo           | Descripcion                                                                        |
| --- | ------------------------- | ----------------- | ---------------------------------------------------------------------------------- |
| 1   | **Analizador Lexico**     | `lexer.py`        | Divide el texto en tokens (palabras clave, operadores, identificadores, etc.)      |
| 2   | **Analizador Sintactico** | `parser.py`       | Verifica la estructura gramatical y construye el AST (Arbol de Sintaxis Abstracta) |
| 3   | **Analizador Semantico**  | `semantic.py`     | Verifica tipos, declaraciones y coherencia logica del programa                     |
| 4   | **Tabla de Simbolos**     | `semantic.py`     | Registra todas las variables declaradas con su tipo y alcance (scope)              |
| 5   | **Codigo Intermedio**     | `intermediate.py` | Genera codigo de tres direcciones (Three-Address Code) a partir del AST            |
| 6   | **Ejecutor de Codigo**    | `executor.py`     | Convierte codigo intermedio a JavaScript ejecutable y lo ejecuta                   |
| 7   | **Traductor**             | `translator.py`   | Traduce codigo JavaScript a EspanolScript (lenguaje natural en espanol)            |
| -   | **Interfaz**              | `main.py`         | Aplicacion de escritorio Tkinter que integra todas las fases                       |

---

## Estructura del proyecto

```
compilador/
  main.py           -> GUI principal (Tkinter)
  lexer.py          -> Analizador lexico (PLY)
  parser.py         -> Analizador sintactico (PLY)
  semantic.py       -> Analizador semantico + tabla de simbolos
  intermediate.py   -> Generador de codigo intermedio
  executor.py       -> Ejecutor de codigo (TAC -> JavaScript)
  translator.py     -> Traductor JS -> EspanolScript
  README.md         -> Esta documentacion
  ESPANOLSCRIPT.md  -> Documentacion completa de EspanolScript
  test_executor.py  -> Script de prueba del ejecutor
```

---

## Como ejecutar

```bash
# Desde la terminal con Anaconda/Python:
python main.py
```

La ventana principal tiene 6 botones:

| Boton                            | Funcion                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| **Analizar**                     | Ejecuta las fases 1-5 (lexico, sintactico, semantico, tabla de simbolos, codigo intermedio) |
| **Tabla de Simbolos**            | Muestra la tabla con todas las variables declaradas, su tipo y alcance                      |
| **Codigo Intermedio**            | Muestra el codigo de tres direcciones generado                                              |
| **Ejecutar Codigo**              | Convierte el codigo intermedio a JavaScript y lo ejecuta con Node.js                       |
| **Traducir JS -> EspanolScript** | Traduce codigo JavaScript a EspanolScript                                                   |
| **Limpiar**                      | Limpia la entrada y los resultados                                                          |

---

## Fase 1: Analizador Lexico

El lexer tokeniza el codigo fuente usando PLY. Reconoce:

### Tokens

| Token                     | Descripcion           | Ejemplo      |
| ------------------------- | --------------------- | ------------ |
| `ID`                      | Identificador         | `miVariable` |
| `NUMERO`                  | Entero o decimal      | `42`, `3.14` |
| `LITERAL_CADENA`          | Cadena entre comillas | `"hola"`     |
| `MAS`                     | Suma                  | `+`          |
| `MENOS`                   | Resta                 | `-`          |
| `POR`                     | Multiplicacion        | `*`          |
| `DIVIDIR`                 | Division              | `/`          |
| `ASIGNAR`                 | Asignacion            | `=`          |
| `IGUAL`                   | Igualdad              | `==`         |
| `DISTINTO`                | Distinto              | `!=`         |
| `MENOR`                   | Menor que             | `<`          |
| `MENOR_IGUAL`             | Menor o igual         | `<=`         |
| `MAYOR`                   | Mayor que             | `>`          |
| `MAYOR_IGUAL`             | Mayor o igual         | `>=`         |
| `PAREN_IZQ` / `PAREN_DER` | Parentesis            | `(` `)`      |
| `LLAVE_IZQ` / `LLAVE_DER` | Llaves                | `{` `}`      |
| `PUNTO_Y_COMA`            | Punto y coma          | `;`          |
| `COMA`                    | Coma                  | `,`          |

### Palabras reservadas

| Token       | Palabra clave |
| ----------- | ------------- |
| `SI`        | `if`          |
| `SINO`      | `else`        |
| `MIENTRAS`  | `while`       |
| `PARA`      | `for`         |
| `RETORNAR`  | `return`      |
| `ENTERO`    | `int`         |
| `FLOTANTE`  | `float`       |
| `CADENA`    | `string`      |
| `BOOLEANO`  | `bool`        |
| `VERDADERO` | `true`        |
| `FALSO`     | `false`       |

---

## Fase 2: Analizador Sintactico

Valida que la secuencia de tokens cumpla la gramatica del lenguaje y construye un AST.

Estructuras soportadas: declaraciones con tipo, asignaciones, `if/else`, `while`, `for`, `return`, bloques `{ }` y expresiones aritmeticas/logicas.

---

## Fase 3: Analizador Semantico

Recorre el AST y verifica:

| #   | Verificacion            | Ejemplo de error                               |
| --- | ----------------------- | ---------------------------------------------- |
| 1   | Variable no declarada   | Usar `x` sin declararla                        |
| 2   | Variable re-declarada   | Declarar `int x;` dos veces en el mismo bloque |
| 3   | Tipos incompatibles     | `int x = "hola";`                              |
| 4   | Operaciones invalidas   | `"hola" - 5`                                   |
| 5   | Comparaciones invalidas | `"abc" == 5`                                   |
| 6   | Negacion invalida       | `-true`                                        |

---

## Fase 4: Tabla de Simbolos

Se genera automaticamente durante el analisis semantico. Registra cada variable declarada con:

- **Nombre**: identificador de la variable
- **Tipo**: `int`, `float`, `string`, `bool`
- **Alcance**: `Global` o `Bloque N` (scope donde fue declarada)

Se puede visualizar presionando el boton "Tabla de Simbolos" despues de analizar.

---

## Fase 5: Generador de Codigo Intermedio

Genera codigo de tres direcciones (TAC - Three-Address Code) legible. Usa:

- **Variables temporales**: `t1`, `t2`, `t3`... para resultados intermedios
- **Etiquetas**: `L1`, `L2`... para control de flujo
- **Instrucciones de salto**: `SI_FALSO`, `IR_A` para condicionales y bucles
- **RETORNAR** para sentencias return

Ejemplo de entrada:

```
int x = 10;
if (x >= 5) {
    x = x + 1;
}
```

Codigo intermedio generado:

```
x = 10
t1 = x >= 5
SI_FALSO t1 IR_A L1
t2 = x + 1
x = t2
L1:
```

---

## Fase 6: Ejecutor de Codigo

El ejecutor toma el codigo intermedio (TAC) y lo convierte de vuelta a **JavaScript ejecutable**. Es capaz de:

1. **Reconocer estructuras de control** (if/else, while) a partir del TAC
2. **Reconstruir el codigo JavaScript** con la logica original
3. **Ejecutar el programa** usando Node.js
4. **Mostrar resultados** en tiempo real

### Como funciona

| Paso | Descripcion |
|------|-------------|
| 1 | Analiza las instrucciones TAC para identificar patrones de control de flujo |
| 2 | Convierte asignaciones (`x = 5`, `t1 = a + b`) a JavaScript |
| 3 | Reconstruye estructuras if/else desde `SI_FALSO` + etiquetas |
| 4 | Reconstruye bucles while desde patrones de etiquetas + saltos |
| 5 | Genera archivo `programa_generado.js` |
| 6 | Ejecuta con `node programa_generado.js` |
| 7 | Captura salida y errores |

### Ejemplo de conversion TAC → JavaScript

**Codigo intermedio (TAC):**
```
x = 10
y = 5
t1 = x + y
resultado = t1
t2 = resultado >= 10
SI_FALSO t2 IR_A L1
t3 = resultado * 2
resultado = t3
L1:
```

**JavaScript generado:**
```javascript
// JavaScript generado automaticamente desde codigo intermedio
// Ejecutar con: node programa_generado.js

let t1, t2, t3;

let x = 10;
let y = 5;
t1 = x + y;
let resultado = t1;
t2 = resultado >= 10;
if (t2) {
    t3 = resultado * 2;
    resultado = t3;
}
```

### Requisitos

Para usar la funcionalidad de ejecucion:
- **Node.js** debe estar instalado y disponible en el PATH
- El programa se ejecuta con un timeout de 10 segundos
- Se genera el archivo `programa_generado.js` en el directorio del compilador

### Ventana de resultados

La ventana de "Resultado de Ejecucion" muestra:
- **Estado**: ✓ Exito o ✗ Error
- **Archivo generado**: Nombre del .js creado
- **Tab Salida**: Output del programa (console.log, prints)
- **Tab Errores**: Errores de ejecucion si los hay
- **Boton "Ver JS Generado"**: Muestra el codigo JavaScript completo

---

## Fase 7: Traductor JavaScript -> EspanolScript

### Que es EspanolScript?

EspanolScript es un lenguaje de programacion **basado en espanol natural** disenado para ser facil de leer y entender. El traductor convierte codigo JavaScript a este lenguaje.

### Tabla de traduccion

#### Variables y valores

| JavaScript         | EspanolScript          |
| ------------------ | ---------------------- |
| `let x = 5;`       | `variable x = 5`       |
| `const PI = 3.14;` | `variable PI = 3.14`   |
| `var name;`        | `variable name = nulo` |
| `true`             | `verdadero`            |
| `false`            | `falso`                |
| `null`             | `nulo`                 |
| `undefined`        | `nulo`                 |

#### Funciones

| JavaScript                   | EspanolScript                     |
| ---------------------------- | --------------------------------- |
| `function sumar(a, b) {`     | `funcion sumar(a, b)`             |
| `async function obtener() {` | `asincrona funcion obtener()`     |
| `const f = (x) => x * 2;`    | `funcion f(x)` + `devolver x * 2` |
| `return resultado;`          | `devolver resultado`              |

#### Condicionales

| JavaScript            | EspanolScript              |
| --------------------- | -------------------------- |
| `if (x > 0) {`        | `si (x > 0) entonces`      |
| `} else if (x < 0) {` | `sino si (x < 0) entonces` |
| `} else {`            | `sino`                     |
| `}`                   | `fin`                      |

#### Bucles

| JavaScript                      | EspanolScript                  |
| ------------------------------- | ------------------------------ |
| `while (cond) {`                | `mientras (cond) hacer`        |
| `for (let i = 0; i < 5; i++) {` | `para i desde 0 hasta 5 hacer` |
| `for (let x of lista) {`        | `para cada x en lista hacer`   |
| `for (let k in obj) {`          | `para cada k en obj hacer`     |

#### Operadores

| JavaScript | EspanolScript |
| ---------- | ------------- |
| `===`      | `==`          |
| `!==`      | `!=`          |
| `&&`       | `y`           |
| `\|\|`     | `o`           |
| `!expr`    | `no expr`     |

#### Impresion y comentarios

| JavaScript          | EspanolScript    |
| ------------------- | ---------------- |
| `console.log(msg);` | `mostrar(msg)`   |
| `// comentario`     | `** comentario`  |
| `/* bloque */`      | `--- bloque ---` |

---

## Ejemplos de prueba

### Ejemplo 1 — Analisis completo (boton "Analizar")

Pegar en el area de entrada:

```
int x = 10;
float y = 3.14;
string nombre = "Juan";
bool activo = true;

if (x >= 5) {
    x = x + 1;
}

int i = 0;
while (i < 3) {
    i = i + 1;
}
```

**Resultado esperado:**

- Tokens: se muestran en la tabla (ENTERO, ID, ASIGNAR, NUMERO, etc.)
- Errores: "Analisis completado sin errores."
- Tabla de simbolos: x(int, Global), y(float, Global), nombre(string, Global), activo(bool, Global), i(int, Global)
- Codigo intermedio: instrucciones de tres direcciones

---

### Ejemplo 2 — Errores semanticos (boton "Analizar")

```
int x = 10;
int x = 5;
int edad = "veinte";
bool activo = true;
if (activo == true) {
    z = 99;
}
```

**Errores esperados:**

- `[Semantico] Variable 'x' ya fue declarada en este bloque.`
- `[Semantico] Tipo incompatible para 'edad': se esperaba 'int', se encontro 'string'.`
- `[Semantico] Variable 'z' no ha sido declarada.`

---

### Ejemplo 3 — Error lexico (boton "Analizar")

```
int $x = 1;
```

**Error esperado:**

- `[Lexico] Caracter inesperado '$' en linea 1, posicion 4.`

---

### Ejemplo 4 — Traduccion JS -> EspanolScript (boton "Traducir")

Pegar en el area de entrada:

```javascript
function sumar(a, b) {
  let resultado = a + b;
  return resultado;
}

let x = 10;
if (x > 5) {
  console.log('mayor que 5');
} else {
  console.log('menor o igual');
}

for (let i = 0; i < 5; i++) {
  console.log(i);
}

while (true) {
  console.log('hola');
}
```

**Resultado esperado en EspanolScript:**

```
funcion sumar(a, b)
    variable resultado = a + b
    devolver resultado
fin

variable x = 10
si (x > 5) entonces
    mostrar("mayor que 5")
sino
    mostrar("menor o igual")
fin

para i desde 0 hasta 5 hacer
    mostrar(i)
fin

mientras (verdadero) hacer
    mostrar("hola")
fin
```

---

### Ejemplo 5 — Traduccion con arrow functions y operadores

```javascript
const doble = (x) => x * 2;

let lista = [1, 2, 3];
for (let num of lista) {
  if (num > 1 && num !== 3) {
    console.log(num);
  }
}

let x = null;
let ok = true;
if (!ok || x === null) {
  console.log('condicion cumplida');
}
```

**Resultado esperado en EspanolScript:**

```
funcion doble(x)
    devolver x * 2

variable lista = [1, 2, 3]
para cada num en lista hacer
    si (num > 1  y  num != 3) entonces
        mostrar(num)
    fin
fin

variable x = nulo
variable ok = verdadero
si (no ok  o  x == nulo) entonces
    mostrar("condicion cumplida")
fin
```

---

L1:
```

---

### Ejemplo 6 — Ejecucion de codigo (boton "Ejecutar Codigo")

**Requisito**: Tener Node.js instalado.

Pegar y presionar "Analizar", luego "Ejecutar Codigo":

```
int a = 5;
int b = 3;
int suma = a + b;

if (suma >= 8) {
    int doble = suma * 2;
    suma = doble;
}

int contador = 0;
while (contador < suma) {
    contador = contador + 1;
}
```

**Resultado esperado:**

- Se genera el archivo `programa_generado.js`
- Se ejecuta automaticamente con Node.js
- Se muestra la ventana con el resultado de ejecucion
- El JavaScript generado contiene las estructuras if/while reconstruidas

**JavaScript generado esperado:**

```javascript
// JavaScript generado automaticamente desde codigo intermedio
// Ejecutar con: node programa_generado.js

let t1, t2, t3, t4, t5;

let a = 5;
let b = 3;
t1 = a + b;
let suma = t1;
t2 = suma >= 8;
if (t2) {
    t3 = suma * 2;
    suma = t3;
}
let contador = 0;
while (t4 = contador < suma) {
    t5 = contador + 1;
    contador = t5;
}
```

---

### Ejemplo 7 — Tabla de simbolos y codigo intermedio

Pegar y presionar "Analizar", luego "Tabla de Simbolos" y "Codigo Intermedio":

```
int a = 5;
float b = 2.5;
float resultado = a + b;
if (resultado >= 7) {
    string msg = "aprobado";
}
```

**Tabla de simbolos esperada:**

| Nombre    | Tipo   | Alcance  |
| --------- | ------ | -------- |
| a         | int    | Global   |
| b         | float  | Global   |
| resultado | float  | Global   |
| msg       | string | Bloque 1 |

**Codigo intermedio esperado:**

```
a = 5
b = 2.5
t1 = a + b
resultado = t1
t2 = resultado >= 7
SI_FALSO t2 IR_A L1
msg = "aprobado"
L1:
```
