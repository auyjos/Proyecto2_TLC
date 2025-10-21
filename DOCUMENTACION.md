# Documentación del Proyecto CYK

## Diseño de la Aplicación

- **Conversión a CNF (`CNFConverter`)**. Maneja la carga de gramáticas, la simplificación completa y la conversión a Forma Normal de Chomsky. El flujo abarca la eliminación de producciones-ε, unitarias y símbolos inútiles, antes de generar reglas auxiliares para terminales o producciones largas.【F:cyk_parser.py†L14-L489】
- **Parser CYK (`CYKParser`)**. Carga gramáticas en CNF y ejecuta el algoritmo CYK guardando, para cada celda de la tabla, los no-terminales que derivan la subcadena y la información necesaria para reconstruir el árbol de derivación.【F:cyk_parser.py†L492-L806】
- **Estructuras principales**:
  - `table[i][j]`: conjunto de no-terminales que generan `words[i:i+j]`.
  - `parse_info[i][j][A]`: tuplas con derivaciones (`('terminal', palabra)` o `('nonterminal', B, C, k)`) para reconstruir el árbol.【F:cyk_parser.py†L628-L697】

## Discusión y Obstáculos

- **Soporte para archivos con BOM**. Algunas gramáticas (por ejemplo, las creadas con editores que añaden BOM) incluían el símbolo `\ufeff`, lo que hacía que el símbolo inicial se almacenara como `\ufeffS`. Esto impedía recuperar el árbol y generaba discrepancias al imprimir reglas. Se normaliza cada línea y producción eliminando la marca BOM antes de tokenizar o dividir reglas.【F:cyk_parser.py†L26-L75】【F:cyk_parser.py†L503-L520】【F:cyk_parser.py†L566-L592】
- **Conversión robusta a CNF**. El convertidor reutiliza no-terminales auxiliares cuando se repiten combinaciones, evitando explosión de reglas y manteniendo la gramática resultante compacta.【F:cyk_parser.py†L124-L437】
- **Reconstrucción del árbol**. El algoritmo estándar solo indica aceptación; por ello se almacena información adicional por celda y se implementa un recorrido recursivo que reconstruye y opcionalmente exporta el árbol en formato DOT.【F:cyk_parser.py†L628-L805】

## Ejemplos y Pruebas

Se ejecutó la conversión oficial y el parser con la gramática de inglés especificada en el enunciado (`exercises/english_grammar.txt`). Tras la conversión, se procesaron frases válidas e inválidas para comprobar el cumplimiento de las especificaciones.【eed869†L1-L70】

| Sentencia                            | Resultado | Tiempo (ms) |
|-------------------------------------|-----------|-------------|
| `she eats a cake with a fork`       | Aceptada  | 0.25        |
| `the cat drinks the beer`           | Aceptada  | 0.23        |
| `he eats`                           | Aceptada  | 0.01        |
| `fork eats the cat`                 | Rechazada | 0.05        |
| `she the eats`                      | Rechazada | 0.02        |

Además, se construyó el árbol de derivación para la frase `she eats a cake with a fork`, verificando que el símbolo inicial correcto (`S`) encabeza la jerarquía tras la normalización del BOM.【eed869†L34-L70】
