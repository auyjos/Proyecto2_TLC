# Ejemplos de Prueba para Gramáticas

Este documento contiene ejemplos de sentencias para probar cada gramática.

---

## 1. grammar_arithmetic.txt
**Descripción:** Expresiones aritméticas con suma, resta, multiplicación y división.

**Sentencias VÁLIDAS:**
- `num + num`
- `num * num + num`
- `( num + num ) * num`
- `id + id * id`
- `( id )`

**Sentencias INVÁLIDAS:**
- `num +`
- `+ num`
- `num num`
- `( num`
- `)`

---

## 2. grammar_balanced_parentheses.txt
**Descripción:** Paréntesis balanceados.

**Sentencias VÁLIDAS:**
- `( )`
- `( ( ) )`
- `( ) ( )`
- `( ( ) ( ) )`
- (vacía - epsilon)

**Sentencias INVÁLIDAS:**
- `(`
- `)`
- `( ( )`
- `( ) )`
- `( ) ( ( )`

---

## 3. grammar_simple_math.txt
**Descripción:** Matemática simple con suma y multiplicación (sin precedencia).

**Sentencias VÁLIDAS:**
- `num + num`
- `num * num`
- `( num )`
- `num + num * num`
- `( num + num ) * num`

**Sentencias INVÁLIDAS:**
- `num +`
- `* num`
- `num num`
- `+ + num`

---

## 4. grammar_boolean.txt
**Descripción:** Expresiones booleanas con and, or, not.

**Sentencias VÁLIDAS:**
- `true`
- `false`
- `true and false`
- `not true`
- `true or false and var`
- `( true or false )`
- `not ( var and true )`

**Sentencias INVÁLIDAS:**
- `and true`
- `true and`
- `not not`
- `true false`

---

## 5. grammar_palindrome.txt
**Descripción:** Palíndromos con 'a' y 'b'.

**Sentencias VÁLIDAS:**
- `a`
- `b`
- `aba`
- `bab`
- `aabaa`
- `bbaabb`
- (vacía - epsilon)

**Sentencias INVÁLIDAS:**
- `ab`
- `ba`
- `aab`
- `abb`
- `abc`

---

## 6. grammar_assignment.txt
**Descripción:** Asignaciones con expresiones aritméticas.

**Sentencias VÁLIDAS:**
- `x = n`
- `y = n + n`
- `z = n * n`
- `x = ( n + n ) * n`
- `y = x + y * z`

**Sentencias INVÁLIDAS:**
- `x =`
- `= n`
- `x + y`
- `x = +`

---

## 7. grammar_anbn.txt
**Descripción:** Lenguaje a^n b^n (igual número de a's y b's).

**Sentencias VÁLIDAS:**
- (vacía - epsilon)
- `a b`
- `a a b b`
- `a a a b b b`

**Sentencias INVÁLIDAS:**
- `a`
- `b`
- `a b a`
- `a a b`
- `a b b`

---

## 8. grammar_spanish_simple.txt
**Descripción:** Frases simples en español.

**Sentencias VÁLIDAS:**
- `el gato come`
- `la niña lee un libro`
- `el perro grande corre`
- `un gato come en la casa`
- `el niño bebe con la niña`

**Sentencias INVÁLIDAS:**
- `gato come el`
- `el come`
- `lee libro`
- `grande perro`

---

## 9. grammar_if_statement.txt
**Descripción:** Sentencias if-then-else.

**Sentencias VÁLIDAS:**
- `if x op y then x = n`
- `if true then x = n`
- `if false then x = n else y = n`
- `if x op y then if true then x = n else y = n`

**Sentencias INVÁLIDAS:**
- `if x then`
- `then x = n`
- `if x op y`
- `x = n else y = n`

---

## 10. grammar_json_simple.txt
**Descripción:** Estructuras JSON simplificadas.

**Sentencias VÁLIDAS:**
- `{ str : str }`
- `{ str : num }`
- `{ str : { str : str } }`
- `{ str : [ str ] }`
- `{ str : str , str : num }`

**Sentencias INVÁLIDAS:**
- `{ str }`
- `{ : str }`
- `{ str : }`
- `str : str`
- `[ ]` (sin objeto contenedor)

---

## Instrucciones de Uso

1. **Convertir a CNF:**
   ```
   Opción 1 del menú
   Archivo de entrada: grammar_arithmetic.txt
   Archivo de salida: grammar_arithmetic_cnf.txt
   ```

2. **Validar sentencias:**
   ```
   Opción 3 del menú
   Ingrese la sentencia según los ejemplos arriba
   ```

3. **Ver árbol de parsing:**
   - Después de una sentencia aceptada, responde 's' para ver el árbol
   - Puedes guardarlo en formato DOT y visualizarlo con Graphviz

---

## Notas Importantes

- Las palabras deben separarse con espacios (ej: `num + num`, no `num+num`)
- Para epsilon (cadena vacía), simplemente presiona Enter sin escribir nada
- Los símbolos multi-carácter (como `num`, `id`, `Det`) se reconocen automáticamente
- Las mayúsculas en las palabras se convierten a minúsculas automáticamente
