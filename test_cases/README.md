# Casos de Prueba para CYK Parser

Este directorio contiene archivos de prueba automáticos para validar gramáticas con el algoritmo CYK.

## Formato de Archivos

Los archivos de prueba deben seguir este formato:

```
# Comentarios empiezan con #
<oración> | <resultado_esperado>
```

Donde `<resultado_esperado>` puede ser:
- `accept` - La oración debe ser aceptada por la gramática
- `reject` - La oración debe ser rechazada por la gramática

## Ejemplo

```
# Casos válidos
she eats a cake | accept
the cat drinks beer | accept

# Casos inválidos
fork eats cat | reject
she the eats | reject
```

## Archivos Disponibles

- **english_grammar_tests.txt** - Pruebas para gramática inglesa simple
- **grammar_anbn_tests.txt** - Pruebas para lenguaje a^n b^n
- **grammar_arithmetic_tests.txt** - Pruebas para expresiones aritméticas
- **grammar_palindrome_tests.txt** - Pruebas para palíndromos
- **grammar_balanced_parentheses_tests.txt** - Pruebas para paréntesis balanceados

## Crear Nuevos Casos de Prueba

1. Crea un archivo con el nombre `<nombre>_tests.txt`
2. Sigue el formato especificado arriba
3. El archivo aparecerá automáticamente en el menú de pruebas (Opción 4)

## Uso

Desde el programa principal:
1. Carga una gramática CNF (opción 1 o 2)
2. Selecciona "Ejecutar ejemplos de prueba" (opción 4)
3. Elige el archivo de pruebas correspondiente a tu gramática
4. Los resultados se mostrarán automáticamente
5. Opcionalmente, exporta los resultados a un archivo
