# 🚀 GUÍA RÁPIDA DE USO

## ¿Las gramáticas vienen en CNF?

**NO.** Las gramáticas están en formato CFG normal (Context-Free Grammar). 

El programa **CONVIERTE AUTOMÁTICAMENTE** de CFG → CNF:
- ✓ Elimina producciones-ε
- ✓ Elimina producciones unitarias
- ✓ Elimina símbolos inútiles
- ✓ Convierte a Forma Normal de Chomsky

---

## 📋 FLUJO COMPLETO

```
Gramática CFG  →  [Conversión Automática]  →  Gramática CNF  →  [Algoritmo CYK]  →  Resultado
(archivo.txt)      (Opción 1 del programa)     (archivo_cnf.txt)    (Opción 3)         (SÍ/NO)
```

---

## 🎯 OPCIÓN 1: Demo Rápido (SIN ESCRIBIR NADA)

### Ejecutar el demo automático:

```bash
python demo_rapido.py
```

**¿Qué hace?**
- ✅ Carga gramáticas automáticamente
- ✅ Convierte a CNF automáticamente
- ✅ Prueba múltiples sentencias automáticamente
- ✅ Muestra árboles de parsing
- ✅ NO pide nombres de archivo

**Menú del demo:**
1. Demo Matemáticas → Prueba `num + num`, `num * num`, etc.
2. Demo Inglés → Prueba `she eats a cake`, etc.
3. Demo Español → Prueba `el gato come`, etc.
4. Ejecutar TODOS

---

## 🎯 OPCIÓN 2: Programa Principal (Con entrada manual)

### Ejecutar el programa completo:

```bash
python cyk_parser.py
```

### Flujo manual paso a paso:

#### PASO 1: Convertir gramática CFG a CNF
```
Opción: 1
Archivo de entrada: grammar_math_direct.txt
Archivo de salida: grammar_math_direct_cnf.txt
```

El programa muestra:
- ✓ Gramática original
- ✓ Paso 1: Eliminando producciones-ε
- ✓ Paso 2: Eliminando producciones unitarias
- ✓ Paso 3: Eliminando símbolos inútiles
- ✓ Paso 4: Convirtiendo a CNF
- ✓ Paso 5: Guardando gramática CNF
- ✓ Gramática final en CNF

#### PASO 2: (Opcional) Cargar CNF existente
```
Opción: 2
Archivo: grammar_math_direct_cnf.txt
```

**Nota:** Si usaste la Opción 1, el programa ya cargó la gramática automáticamente.

#### PASO 3: Validar sentencias
```
Opción: 3
Ingrese la sentencia: num + num
```

El programa muestra:
- ✓ Análisis paso a paso del algoritmo CYK
- ✓ Tabla de parsing
- ✓ Resultado: ACEPTADA/RECHAZADA
- ✓ Tiempo de ejecución
- ✓ Opción de ver árbol de parsing

#### PASO 4: (Opcional) Ver árbol
```
¿Desea ver el árbol de parsing? s
```

Muestra el árbol jerárquico en consola.

```
¿Guardar árbol en formato DOT? s
Nombre del archivo: tree.dot
```

Para visualizar con Graphviz:
```bash
dot -Tpng tree.dot -o tree.png
```

---

## 📁 GRAMÁTICAS DISPONIBLES

### Para Matemáticas:
- ✅ **`grammar_math_direct.txt`** (RECOMENDADO - simple y funciona bien)
- `grammar_simple_math.txt`
- `grammar_arithmetic.txt` (complejo, muchas reglas en CNF)

### Para Lenguaje Natural:
- ✅ **`english_grammar.txt`** (RECOMENDADO - ya probado)
- ✅ **`grammar_spanish_simple.txt`** (español básico)

### Otras:
- `grammar_balanced_parentheses.txt`
- `grammar_boolean.txt`
- `grammar_palindrome.txt`
- `grammar_assignment.txt`
- `grammar_anbn.txt`
- `grammar_if_statement.txt`
- `grammar_json_simple.txt`

---

## 💡 EJEMPLOS RÁPIDOS

### Ejemplo 1: Matemáticas (Demo Rápido)
```bash
python demo_rapido.py
Opción: 1
```

### Ejemplo 2: Inglés (Demo Rápido)
```bash
python demo_rapido.py
Opción: 2
```

### Ejemplo 3: Manual completo
```bash
python cyk_parser.py
Opción: 1
  Entrada: english_grammar.txt
  Salida: english_grammar_cnf.txt
Opción: 3
  Sentencia: she eats a cake with a fork
  ¿Ver árbol? s
  ¿Guardar? s
  Archivo: my_tree.dot
```

---

## 🔑 DIFERENCIAS CLAVE

| Característica | demo_rapido.py | cyk_parser.py |
|---------------|----------------|---------------|
| Entrada de archivos | ❌ Automático | ✅ Manual |
| Conversión CFG→CNF | ✅ Automática | ✅ Manual (Opción 1) |
| Pruebas múltiples | ✅ Automáticas | ❌ Una por una |
| Árboles de parsing | ✅ Muestra auto | ✅ Opcional |
| Ideal para | Demostración rápida | Uso interactivo |

---

## ⚡ RECOMENDACIÓN

### Para probar rápido:
```bash
python demo_rapido.py
```

### Para uso completo e interactivo:
```bash
python cyk_parser.py
```

---

## 🎯 RESUMEN DEL FLUJO

1. **Tienes una gramática CFG** (formato normal, no CNF)
2. **El programa convierte** automáticamente a CNF (Opción 1)
3. **El programa parsea** con CYK usando la CNF (Opción 3)
4. **Muestra resultado** + tiempo + árbol

**NO necesitas hacer la conversión manualmente** - el programa lo hace todo. ✨
