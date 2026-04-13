# EspanolScript — Documentacion del Lenguaje

## Que es EspanolScript?

EspanolScript es un **lenguaje de programacion basado en espanol natural**, disenado para ser facil de leer y entender. Es el lenguaje destino del compilador: el traductor convierte codigo **JavaScript** a EspanolScript.

EspanolScript no usa llaves `{ }` ni punto y coma `;`. En su lugar usa palabras como `entonces`, `hacer`, `fin`, `devolver`, etc. Cualquier persona que hable espanol puede leer un programa en EspanolScript y entender que hace sin conocimiento previo de programacion.

---

## Sintaxis completa

### 1. Variables

Para declarar una variable se usa la palabra `variable`:

```
variable nombre = "Juan"
variable edad = 25
variable precio = 99.99
variable activo = verdadero
variable dato = nulo
```

**Reglas:**

- No se necesita especificar el tipo (se infiere del valor)
- No se usa punto y coma al final
- `nulo` equivale a un valor vacio o inexistente

---

### 2. Tipos de datos

| Tipo            | Ejemplo              | Descripcion                 |
| --------------- | -------------------- | --------------------------- |
| Numero entero   | `42`                 | Numeros sin decimales       |
| Numero decimal  | `3.14`               | Numeros con punto decimal   |
| Cadena de texto | `"Hola mundo"`       | Texto entre comillas dobles |
| Booleano        | `verdadero`, `falso` | Valores logicos de verdad   |
| Nulo            | `nulo`               | Ausencia de valor           |

---

### 3. Operadores

#### Operadores aritmeticos

| Operador | Significado    | Ejemplo |
| -------- | -------------- | ------- |
| `+`      | Suma           | `a + b` |
| `-`      | Resta          | `a - b` |
| `*`      | Multiplicacion | `a * b` |
| `/`      | Division       | `a / b` |

#### Operadores de comparacion

| Operador | Significado   | Ejemplo   |
| -------- | ------------- | --------- |
| `==`     | Igual a       | `x == 5`  |
| `!=`     | Distinto de   | `x != 0`  |
| `<`      | Menor que     | `x < 10`  |
| `<=`     | Menor o igual | `x <= 10` |
| `>`      | Mayor que     | `x > 0`   |
| `>=`     | Mayor o igual | `x >= 1`  |

#### Operadores logicos

| Operador | Significado                       | Ejemplo           |
| -------- | --------------------------------- | ----------------- |
| `y`      | Y logico (ambos verdaderos)       | `x > 0 y x < 10`  |
| `o`      | O logico (al menos uno verdadero) | `x == 0 o x == 1` |
| `no`     | Negacion                          | `no activo`       |

---

### 4. Condicionales

#### Si / sino

```
si (condicion) entonces
    ** codigo si la condicion es verdadera
fin
```

#### Si / sino si / sino

```
si (edad >= 18) entonces
    mostrar("Mayor de edad")
sino si (edad >= 13) entonces
    mostrar("Adolescente")
sino
    mostrar("Nino")
fin
```

**Reglas:**

- La condicion va entre parentesis
- Se usa `entonces` para abrir el bloque
- Se usa `fin` para cerrar el bloque
- `sino si` permite evaluar otra condicion
- `sino` se ejecuta si ninguna condicion anterior fue verdadera

---

### 5. Bucles

#### Mientras (while)

Repite mientras la condicion sea verdadera:

```
mientras (condicion) hacer
    ** codigo que se repite
fin
```

Ejemplo:

```
variable contador = 0
mientras (contador < 5) hacer
    mostrar(contador)
    contador = contador + 1
fin
```

#### Para (for clasico)

Repite desde un valor inicial hasta un valor final:

```
para i desde 0 hasta 10 hacer
    mostrar(i)
fin
```

Con paso personalizado:

```
para i desde 0 hasta 20 con paso 2 hacer
    mostrar(i)
fin
```

Conteo regresivo:

```
para i desde 10 hasta 0 con paso -1 hacer
    mostrar(i)
fin
```

#### Para cada (for...of / for...in)

Recorre cada elemento de una lista u objeto:

```
para cada elemento en lista hacer
    mostrar(elemento)
fin
```

```
para cada clave en objeto hacer
    mostrar(clave)
fin
```

---

### 6. Funciones

#### Declaracion de funciones

```
funcion nombre(parametro1, parametro2)
    ** cuerpo de la funcion
    devolver resultado
fin
```

Ejemplo:

```
funcion sumar(a, b)
    variable resultado = a + b
    devolver resultado
fin
```

#### Funciones asincronas

```
asincrona funcion obtenerDatos(url)
    ** codigo asincrono
    devolver datos
fin
```

#### Funciones cortas (flecha)

Cuando la funcion solo devuelve una expresion:

```
funcion doble(x)
    devolver x * 2
```

---

### 7. Entrada/Salida

#### Mostrar en pantalla

```
mostrar("Hola mundo")
mostrar("El resultado es:", resultado)
mostrar(variable1, variable2)
```

`mostrar` es el equivalente a `console.log` en JavaScript.

---

### 8. Comentarios

#### Comentario de una linea

```
** Este es un comentario de una linea
variable x = 5  ** tambien puede ir al final de una linea
```

#### Comentario de varias lineas

```
--- Este es un comentario
    que ocupa varias lineas ---
```

---

### 9. Listas y objetos

EspanolScript mantiene la misma sintaxis de JavaScript para listas y objetos:

```
variable numeros = [1, 2, 3, 4, 5]
variable persona = {nombre: "Ana", edad: 30}
```

---

## Tabla de traduccion completa: JavaScript -> EspanolScript

### Palabras clave

| JavaScript              | EspanolScript                  |
| ----------------------- | ------------------------------ |
| `let` / `const` / `var` | `variable`                     |
| `function`              | `funcion`                      |
| `async function`        | `asincrona funcion`            |
| `return`                | `devolver`                     |
| `if (...) {`            | `si (...) entonces`            |
| `else if (...) {`       | `sino si (...) entonces`       |
| `else {`                | `sino`                         |
| `}` (cierre de bloque)  | `fin`                          |
| `while (...) {`         | `mientras (...) hacer`         |
| `for (i=0; i<n; i++) {` | `para i desde 0 hasta n hacer` |
| `for (x of lista) {`    | `para cada x en lista hacer`   |
| `for (k in obj) {`      | `para cada k en obj hacer`     |
| `console.log(...)`      | `mostrar(...)`                 |

### Valores

| JavaScript  | EspanolScript |
| ----------- | ------------- |
| `true`      | `verdadero`   |
| `false`     | `falso`       |
| `null`      | `nulo`        |
| `undefined` | `nulo`        |

### Operadores logicos

| JavaScript | EspanolScript |
| ---------- | ------------- |
| `&&`       | `y`           |
| `\|\|`     | `o`           |
| `!`        | `no`          |
| `===`      | `==`          |
| `!==`      | `!=`          |

### Comentarios

| JavaScript    | EspanolScript   |
| ------------- | --------------- |
| `// texto`    | `** texto`      |
| `/* texto */` | `--- texto ---` |

### Template literals

| JavaScript             | EspanolScript     |
| ---------------------- | ----------------- |
| `` `Hola ${nombre}` `` | `"Hola {nombre}"` |

---

## Programas de ejemplo

### Ejemplo 1 — Hola Mundo

```
mostrar("Hola Mundo!")
```

### Ejemplo 2 — Calculadora basica

```
funcion sumar(a, b)
    devolver a + b
fin

funcion restar(a, b)
    devolver a - b
fin

funcion multiplicar(a, b)
    devolver a * b
fin

funcion dividir(a, b)
    si (b != 0) entonces
        devolver a / b
    sino
        mostrar("Error: division entre cero")
        devolver 0
    fin
fin

variable x = 10
variable y = 3
mostrar("Suma:", sumar(x, y))
mostrar("Resta:", restar(x, y))
mostrar("Producto:", multiplicar(x, y))
mostrar("Division:", dividir(x, y))
```

### Ejemplo 3 — Numeros pares

```
mostrar("Numeros pares del 0 al 20:")
para i desde 0 hasta 20 con paso 2 hacer
    mostrar(i)
fin
```

### Ejemplo 4 — Buscar en una lista

```
variable frutas = ["manzana", "banana", "naranja", "uva"]
variable buscada = "naranja"
variable encontrada = falso

para cada fruta en frutas hacer
    si (fruta == buscada) entonces
        mostrar("Fruta encontrada:", fruta)
        encontrada = verdadero
    fin
fin

si (no encontrada) entonces
    mostrar("La fruta no esta en la lista")
fin
```

### Ejemplo 5 — Factorial

```
funcion factorial(n)
    si (n <= 1) entonces
        devolver 1
    fin
    devolver n * factorial(n - 1)
fin

para i desde 1 hasta 10 hacer
    mostrar("Factorial de", i, "es", factorial(i))
fin
```

### Ejemplo 6 — Clasificacion de temperatura

```
funcion clasificar(temp)
    si (temp >= 35) entonces
        devolver "Muy caliente"
    sino si (temp >= 25) entonces
        devolver "Calido"
    sino si (temp >= 15) entonces
        devolver "Templado"
    sino si (temp >= 5) entonces
        devolver "Frio"
    sino
        devolver "Muy frio"
    fin
fin

variable temperaturas = [40, 28, 18, 8, -2]
para cada temp en temperaturas hacer
    mostrar(temp, "grados:", clasificar(temp))
fin
```

### Ejemplo 7 — Contador con mientras

```
variable contador = 10
mostrar("Cuenta regresiva:")
mientras (contador >= 0) hacer
    mostrar(contador)
    contador = contador - 1
fin
mostrar("Despegue!")
```

---

## Equivalencia rapida JavaScript -> EspanolScript

```javascript
// JavaScript                          // EspanolScript
function saludar(nombre) {             funcion saludar(nombre)
    if (nombre === null) {                 si (nombre == nulo) entonces
        console.log("Hola!");                  mostrar("Hola!")
    } else {                               sino
        console.log(`Hola ${nombre}`);         mostrar("Hola {nombre}")
    }                                      fin
}                                      fin

let activo = true;                     variable activo = verdadero
while (activo) {                       mientras (activo) hacer
    console.log("corriendo");              mostrar("corriendo")
    activo = false;                        activo = falso
}                                      fin

for (let i = 0; i < 5; i++) {         para i desde 0 hasta 5 hacer
    console.log(i);                        mostrar(i)
}                                      fin
```
