"""
Proyecto 2 - Algoritmo CYK (Cocke-Younger-Kasami)
Teoría de la Computación
Implementación del algoritmo CYK para parsing de gramáticas CFG
"""

import os
import re
import time
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


class CNFConverter:
    """
    Convierte una gramática CFG a Forma Normal de Chomsky (CNF).
    Incluye eliminación de ε-producciones, producciones unitarias, y símbolos inútiles.
    """
    
    def __init__(self):
        self.productions = {}  # Dict[str, List[str]]
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = 'S'
        
    def parse_grammar_line(self, line: str) -> Tuple[str, List[str]]:
        """
        Parsea una línea de gramática.
        Formato: A -> alpha | beta | gamma
        Soporta símbolos multi-carácter (ej: id, num) y símbolos especiales (+, *, etc.)
        """
        line = line.strip()
        if not line or line.startswith('#'):
            return None, []
        
        # Soportar tanto -> como →
        if '→' in line:
            parts = line.split('→')
        elif '->' in line:
            parts = line.split('->')
        else:
            return None, []
        
        if len(parts) != 2:
            return None, []
        
        left = parts[0].strip()
        right = parts[1].strip()
        
        # Dividir por |
        productions = [p.strip() for p in right.split('|')]
        
        return left, productions
    
    def tokenize_production(self, prod: str) -> List[str]:
        """
        Tokeniza una producción en símbolos individuales.
        Maneja símbolos multi-carácter como 'id', 'num', 'Det', 'NP', 'VP', etc.
        
        Reglas:
        - Palabras que empiezan con MAYÚSCULA (S, NP, VP, Det, etc.) = no-terminales
        - Palabras minúsculas (id, num, he, she, cat, etc.) = terminales
        - Símbolos especiales (+, *, (, ), etc.) = terminales
        - 'e' o 'ε' = epsilon
        """
        if prod in ['ε', 'e', '']:
            return ['ε']
        
        symbols = []
        i = 0
        while i < len(prod):
            # Saltar espacios
            if prod[i].isspace():
                i += 1
                continue
            
            # No-terminal (empieza con mayúscula, puede tener minúsculas: S, NP, VP, Det)
            if prod[i].isupper():
                j = i + 1
                # Continuar mientras sean letras (mayúsculas o minúsculas)
                while j < len(prod) and prod[j].isalpha():
                    j += 1
                symbols.append(prod[i:j])
                i = j
            
            # Terminal multi-carácter (palabra minúscula como 'id', 'num', 'he', 'cat')
            elif prod[i].islower():
                j = i
                while j < len(prod) and prod[j].islower():
                    j += 1
                symbols.append(prod[i:j])
                i = j
            
            # Símbolo especial (+, *, (, ), etc.)
            else:
                symbols.append(prod[i])
                i += 1
        
        return symbols
    
    def load_grammar(self, filename: str) -> bool:
        """
        Carga una gramática desde un archivo.
        """
        try:
            if not os.path.exists(filename):
                print(f"Error: El archivo {filename} no existe.")
                return False
            
            self.productions.clear()
            self.non_terminals.clear()
            self.terminals.clear()
            
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    left, prods = self.parse_grammar_line(line)
                    if left is None:
                        continue
                    
                    self.non_terminals.add(left)
                    
                    if left not in self.productions:
                        self.productions[left] = []
                    
                    for prod in prods:
                        # Tokenizar la producción
                        symbols = self.tokenize_production(prod)
                        prod_string = ' '.join(symbols)
                        
                        if prod_string not in self.productions[left]:
                            self.productions[left].append(prod_string)
                        
                        # Identificar terminales y no-terminales
                        for symbol in symbols:
                            if symbol in ['ε', 'e']:
                                continue
                            elif len(symbol) == 1 and symbol[0].isupper():
                                self.non_terminals.add(symbol)
                            else:
                                self.terminals.add(symbol)
            
            # El símbolo inicial es el primero que aparece
            if self.productions:
                self.start_symbol = list(self.productions.keys())[0]
            
            print(f"✓ Gramática cargada: {len(self.productions)} no-terminales, {len(self.terminals)} terminales")
            return True
            
        except Exception as e:
            print(f"Error al cargar gramática: {e}")
            return False
    
    def display_grammar(self, title="GRAMÁTICA"):
        """
        Muestra la gramática actual.
        """
        print(f"\n{'='*60}")
        print(f"{title:^60}")
        print('='*60)
        for nt in sorted(self.productions.keys()):
            prods = " | ".join(self.productions[nt])
            print(f"{nt} → {prods}")
        print('='*60)
    
    def find_nullable_symbols(self) -> Set[str]:
        """
        Encuentra símbolos anulables (que pueden derivar en ε).
        """
        nullable = set()
        
        # Paso 1: Símbolos con producción ε directa
        for nt, prods in self.productions.items():
            for prod in prods:
                if prod == 'ε' or prod == 'e' or prod == '':
                    nullable.add(nt)
                    break
        
        # Paso 2: Símbolos que derivan solo en anulables
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt not in nullable:
                    for prod in prods:
                        if prod != 'ε' and prod != 'e' and prod != '':
                            symbols = prod.split()
                            if all(s in nullable for s in symbols):
                                nullable.add(nt)
                                changed = True
                                break
        
        return nullable
    
    def remove_epsilon_productions(self):
        """
        Elimina producciones-ε de la gramática.
        """
        print("\n[1/5] Eliminando producciones-ε...")
        
        nullable = self.find_nullable_symbols()
        if not nullable:
            print("  → No hay símbolos anulables")
            return
        
        print(f"  → Símbolos anulables: {sorted(nullable)}")
        
        new_grammar = {}
        
        for nt, prods in self.productions.items():
            new_prods = set()
            
            for prod in prods:
                if prod == 'ε' or prod == 'e' or prod == '':
                    # Si es el símbolo inicial, permitir ε
                    if nt == self.start_symbol:
                        new_prods.add('ε')
                    continue
                
                symbols = prod.split()
                
                # Generar todas las combinaciones removiendo anulables
                nullable_positions = [i for i, s in enumerate(symbols) if s in nullable]
                
                # 2^n combinaciones
                for mask in range(1 << len(nullable_positions)):
                    new_prod = []
                    for i, symbol in enumerate(symbols):
                        if i in nullable_positions:
                            pos_index = nullable_positions.index(i)
                            if not (mask & (1 << pos_index)):
                                new_prod.append(symbol)
                        else:
                            new_prod.append(symbol)
                    
                    if new_prod:
                        new_prods.add(' '.join(new_prod))
                    elif nt == self.start_symbol:
                        new_prods.add('ε')
            
            new_grammar[nt] = list(new_prods)
        
        self.productions = new_grammar
        print(f"  ✓ Producciones-ε eliminadas")
    
    def remove_unit_productions(self):
        """
        Elimina producciones unitarias (A → B).
        """
        print("\n[2/5] Eliminando producciones unitarias...")
        
        # Encontrar todas las producciones unitarias
        unit_pairs = set()
        for nt, prods in self.productions.items():
            for prod in prods:
                symbols = prod.split()
                if len(symbols) == 1 and symbols[0] in self.non_terminals:
                    unit_pairs.add((nt, symbols[0]))
        
        # Clausura transitiva
        changed = True
        while changed:
            changed = False
            new_pairs = set()
            for (a, b) in unit_pairs:
                for (c, d) in unit_pairs:
                    if b == c and (a, d) not in unit_pairs:
                        new_pairs.add((a, d))
                        changed = True
            unit_pairs.update(new_pairs)
        
        # Reemplazar producciones unitarias
        new_grammar = {}
        for nt in self.productions.keys():
            new_prods = set()
            
            # Agregar producciones no unitarias
            for prod in self.productions[nt]:
                symbols = prod.split()
                if len(symbols) != 1 or symbols[0] not in self.non_terminals:
                    new_prods.add(prod)
            
            # Agregar producciones derivadas de unitarias
            for (a, b) in unit_pairs:
                if a == nt:
                    for prod in self.productions[b]:
                        symbols = prod.split()
                        if len(symbols) != 1 or symbols[0] not in self.non_terminals:
                            new_prods.add(prod)
            
            new_grammar[nt] = list(new_prods)
        
        self.productions = new_grammar
        print(f"  ✓ Producciones unitarias eliminadas")
    
    def remove_useless_symbols(self):
        """
        Elimina símbolos inútiles (que no generan terminales o no son alcanzables).
        """
        print("\n[3/5] Eliminando símbolos inútiles...")
        
        # Paso 1: Encontrar símbolos generadores (que derivan en terminales)
        generating = set()
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt not in generating:
                    for prod in prods:
                        if prod == 'ε':
                            generating.add(nt)
                            changed = True
                            break
                        symbols = prod.split()
                        if all(s in self.terminals or s in generating for s in symbols):
                            generating.add(nt)
                            changed = True
                            break
        
        # Paso 2: Encontrar símbolos alcanzables desde S
        reachable = {self.start_symbol}
        changed = True
        while changed:
            changed = False
            for nt in list(reachable):
                if nt in self.productions:
                    for prod in self.productions[nt]:
                        symbols = prod.split()
                        for s in symbols:
                            if s in self.non_terminals and s not in reachable:
                                reachable.add(s)
                                changed = True
        
        # Símbolos útiles = generadores ∩ alcanzables
        useful = generating & reachable
        
        # Eliminar símbolos inútiles
        new_grammar = {}
        for nt in useful:
            if nt in self.productions:
                new_prods = []
                for prod in self.productions[nt]:
                    symbols = prod.split()
                    if all(s in self.terminals or s in useful for s in symbols):
                        new_prods.append(prod)
                if new_prods:
                    new_grammar[nt] = new_prods
        
        self.productions = new_grammar
        self.non_terminals = useful
        print(f"  ✓ Símbolos inútiles eliminados")
    
    def convert_to_cnf(self):
        """
        Convierte la gramática a Forma Normal de Chomsky.
        CNF: A → BC (dos no-terminales) o A → a (un terminal)
        """
        print("\n[4/5] Convirtiendo a Forma Normal de Chomsky...")
        
        new_grammar = {}
        terminal_map = {}  # terminal -> no-terminal
        intermediate_map = {}  # producción -> no-terminal (NUEVO: para reutilizar)
        next_nt_index = [0]  # Para generar nuevos no-terminales
        
        def get_new_nonterminal(base='X'):
            """Genera un nuevo no-terminal único."""
            while True:
                name = f"{base}{next_nt_index[0]}"
                next_nt_index[0] += 1
                if name not in self.non_terminals and name not in new_grammar:
                    self.non_terminals.add(name)
                    return name
        
        def get_terminal_nonterminal(terminal):
            """Obtiene o crea un no-terminal para un terminal."""
            if terminal not in terminal_map:
                new_nt = get_new_nonterminal('T')
                terminal_map[terminal] = new_nt
                new_grammar[new_nt] = [terminal]
            return terminal_map[terminal]
        
        def get_intermediate_nonterminal(production):
            """Obtiene o crea un no-terminal para una producción intermedia.
            OPTIMIZACIÓN: Reutiliza no-terminales para producciones idénticas."""
            if production not in intermediate_map:
                new_nt = get_new_nonterminal('Y')
                intermediate_map[production] = new_nt
                new_grammar[new_nt] = [production]
            return intermediate_map[production]
        
        # Procesar cada producción
        for nt, prods in self.productions.items():
            new_prods = []
            
            for prod in prods:
                if prod == 'ε':
                    if nt == self.start_symbol:
                        new_prods.append('ε')
                    continue
                
                symbols = prod.split()
                
                # Caso 1: A → a (terminal único) - ya está en CNF
                if len(symbols) == 1 and symbols[0] in self.terminals:
                    new_prods.append(prod)
                
                # Caso 2: A → BC (dos no-terminales) - ya está en CNF
                elif len(symbols) == 2 and all(s in self.non_terminals for s in symbols):
                    new_prods.append(prod)
                
                # Caso 3: Necesita conversión
                else:
                    # Reemplazar terminales por no-terminales
                    converted_symbols = []
                    for symbol in symbols:
                        if symbol in self.terminals:
                            converted_symbols.append(get_terminal_nonterminal(symbol))
                        else:
                            converted_symbols.append(symbol)
                    
                    # Si hay más de 2 símbolos, crear producciones intermedias
                    while len(converted_symbols) > 2:
                        # OPTIMIZACIÓN: Reutilizar no-terminal si la producción ya existe
                        last_two = ' '.join(converted_symbols[-2:])
                        new_nt = get_intermediate_nonterminal(last_two)
                        converted_symbols = converted_symbols[:-2] + [new_nt]
                    
                    new_prods.append(' '.join(converted_symbols))
            
            new_grammar[nt] = new_prods
        
        self.productions = new_grammar
        print(f"  ✓ Gramática convertida a CNF")
        print(f"    - Nuevos no-terminales para terminales: {len(terminal_map)}")
        print(f"    - Nuevos no-terminales intermedios: {len(intermediate_map)}")
        print(f"    - Reglas optimizadas (sin duplicados)")
        
        # Eliminar producciones unitarias que pudieron haberse creado
        self.remove_unit_productions()
    
    def save_cnf_grammar(self, filename: str):
        """
        Guarda la gramática en CNF a un archivo.
        """
        print(f"\n[5/5] Guardando gramática en CNF...")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Escribir el símbolo inicial primero
                if self.start_symbol in self.productions:
                    prods = " | ".join(self.productions[self.start_symbol])
                    f.write(f"{self.start_symbol} -> {prods}\n")
                
                # Escribir el resto en orden alfabético
                for nt in sorted(self.productions.keys()):
                    if nt != self.start_symbol:
                        prods = " | ".join(self.productions[nt])
                        f.write(f"{nt} -> {prods}\n")
            print(f"  ✓ Guardada en: {filename}")
            return True
        except Exception as e:
            print(f"  ✗ Error al guardar: {e}")
            return False
    
    def full_conversion(self, input_file: str, output_file: str) -> bool:
        """
        Proceso completo: carga gramática, convierte a CNF, y guarda.
        """
        print("\n" + "="*60)
        print("CONVERSIÓN A FORMA NORMAL DE CHOMSKY")
        print("="*60)
        
        if not self.load_grammar(input_file):
            return False
        
        self.display_grammar("GRAMÁTICA ORIGINAL")
        
        self.remove_epsilon_productions()
        self.remove_unit_productions()
        self.remove_useless_symbols()
        self.convert_to_cnf()
        
        self.display_grammar("GRAMÁTICA EN CNF")
        
        return self.save_cnf_grammar(output_file)


class CYKParser:
    """
    Implementación del algoritmo CYK para parsing de gramáticas en CNF.
    """
    
    def __init__(self):
        self.grammar = {}  # Dict[str, List[List[str]]]
        self.terminal_rules = {}  # Dict[str, List[str]] - terminal -> [non-terminals]
        self.nonterminal_rules = {}  # Dict[Tuple[str,str], List[str]]
        self.start_symbol = 'S'
    
    def tokenize_production(self, prod: str) -> List[str]:
        """
        Tokeniza una producción en símbolos individuales.
        Maneja símbolos multi-carácter como 'id', 'num', 'Det', 'NP', 'VP', etc.
        
        Reglas:
        - Palabras que empiezan con MAYÚSCULA (S, NP, VP, Det, etc.) = no-terminales
        - Palabras minúsculas (id, num, he, she, cat, etc.) = terminales
        - Símbolos especiales (+, *, (, ), etc.) = terminales
        - 'e' o 'ε' = epsilon
        """
        # Si ya está separado por espacios, usarlo directamente
        if ' ' in prod:
            return prod.split()
        
        if prod in ['ε', 'e', '']:
            return ['ε']
        
        symbols = []
        i = 0
        while i < len(prod):
            # Saltar espacios
            if prod[i].isspace():
                i += 1
                continue
            
            # No-terminal (empieza con mayúscula, puede tener minúsculas: S, NP, VP, Det)
            if prod[i].isupper():
                j = i + 1
                # Continuar mientras sean letras (mayúsculas o minúsculas)
                while j < len(prod) and prod[j].isalpha():
                    j += 1
                symbols.append(prod[i:j])
                i = j
            
            # Terminal multi-carácter (palabra minúscula como 'id', 'num', 'he', 'cat')
            elif prod[i].islower():
                j = i
                while j < len(prod) and prod[j].islower():
                    j += 1
                symbols.append(prod[i:j])
                i = j
            
            # Símbolo especial (+, *, (, ), etc.)
            else:
                symbols.append(prod[i])
                i += 1
        
        return symbols
        
    def load_cnf_grammar(self, filename: str) -> bool:
        """
        Carga una gramática en CNF.
        """
        try:
            self.grammar.clear()
            self.terminal_rules.clear()
            self.nonterminal_rules.clear()
            
            first_nonterminal = None
            
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parsear: A -> B C | a
                    if '→' in line:
                        parts = line.split('→')
                    elif '->' in line:
                        parts = line.split('->')
                    else:
                        continue
                    
                    left = parts[0].strip()
                    right = parts[1].strip()
                    
                    # Guardar el primer no-terminal como símbolo inicial (usualmente S)
                    if first_nonterminal is None:
                        first_nonterminal = left
                    
                    if left not in self.grammar:
                        self.grammar[left] = []
                    
                    for prod in right.split('|'):
                        prod = prod.strip()
                        # Tokenizar la producción para manejar símbolos multi-carácter
                        symbols = self.tokenize_production(prod)
                        
                        self.grammar[left].append(symbols)
                        
                        # Indexar por tipo de producción
                        if len(symbols) == 1:
                            # A -> a (terminal)
                            terminal = symbols[0]
                            if terminal not in self.terminal_rules:
                                self.terminal_rules[terminal] = []
                            self.terminal_rules[terminal].append(left)
                        elif len(symbols) == 2:
                            # A -> B C
                            pair = (symbols[0], symbols[1])
                            if pair not in self.nonterminal_rules:
                                self.nonterminal_rules[pair] = []
                            self.nonterminal_rules[pair].append(left)
            
            # Establecer el símbolo inicial (primero en el archivo, no alfabéticamente)
            if first_nonterminal:
                self.start_symbol = first_nonterminal
            
            print(f"✓ Gramática CNF cargada: {len(self.grammar)} reglas")
            return True
            
        except Exception as e:
            print(f"Error al cargar gramática CNF: {e}")
            return False
    
    def parse(self, sentence: str, verbose=True) -> Tuple[bool, float, Optional[dict]]:
        """
        Algoritmo CYK para determinar si una oracion pertenece al lenguaje.
        
        Retorna: (acepta: bool, tiempo: float, tabla: dict)
        """
        words = sentence.lower().split()
        n = len(words)
        
        if n == 0:
            return False, 0.0, None
        
        start_time = time.time()
        
        # Tabla CYK: table[i][j] = conjunto de no-terminales que derivan words[i:i+j]
        # Guardamos también el parse tree
        table = [[set() for _ in range(n + 1)] for _ in range(n)]
        parse_info = [[{} for _ in range(n + 1)] for _ in range(n)]
        
        # Paso 1: Llenar la diagonal (subcadenas de longitud 1)
        if verbose:
            print(f"\n{'='*60}")
            print("ALGORITMO CYK - ANÁLISIS")
            print('='*60)
            print(f"Oracion: {sentence}")
            print(f"Palabras: {words}")
            print(f"\nPaso 1: Subcadenas de longitud 1")
        
        for i in range(n):
            word = words[i]
            if word in self.terminal_rules:
                for nt in self.terminal_rules[word]:
                    table[i][1].add(nt)
                    parse_info[i][1][nt] = ('terminal', word)
                    if verbose:
                        print(f"  [{i},{i+1}] '{word}' -> {nt}")
        
        # Paso 2: Llenar la tabla para subcadenas de longitud 2 a n
        for length in range(2, n + 1):
            if verbose:
                print(f"\nPaso {length}: Subcadenas de longitud {length}")
            
            for i in range(n - length + 1):
                j = i + length
                
                # Probar todas las particiones
                for k in range(i + 1, j):
                    # Subcadena [i,k) y [k,j)
                    left_symbols = table[i][k - i]
                    right_symbols = table[k][j - k]
                    
                    # Buscar producciones A -> B C donde B ∈ left, C ∈ right
                    for B in left_symbols:
                        for C in right_symbols:
                            if (B, C) in self.nonterminal_rules:
                                for A in self.nonterminal_rules[(B, C)]:
                                    if A not in table[i][j - i]:
                                        table[i][j - i].add(A)
                                        parse_info[i][j - i][A] = ('nonterminal', B, C, k)
                                        if verbose:
                                            substr = ' '.join(words[i:j])
                                            print(f"  [{i},{j}] '{substr}' -> {A} (via {B} {C}, k={k})")
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Verificar si el símbolo inicial está en table[0][n]
        accepted = self.start_symbol in table[0][n]
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"RESULTADO: {'✓ ACEPTADA' if accepted else '✗ RECHAZADA'}")
            print(f"Tiempo de ejecución: {elapsed*1000:.4f} ms")
            print('='*60)
        
        return accepted, elapsed, {'table': table, 'parse_info': parse_info, 'words': words}
    
    def build_parse_tree(self, parse_data: dict, symbol: str = None, i: int = 0, j: int = None) -> dict:
        """
        Construye el árbol de parsing a partir de la tabla CYK.
        """
        if symbol is None:
            symbol = self.start_symbol
        
        words = parse_data['words']
        n = len(words)
        
        if j is None:
            j = n
        
        table = parse_data['table']
        parse_info = parse_data['parse_info']
        
        length = j - i
        
        if symbol not in parse_info[i][length]:
            return None
        
        info = parse_info[i][length][symbol]
        
        if info[0] == 'terminal':
            # Nodo hoja
            return {
                'symbol': symbol,
                'type': 'terminal',
                'value': info[1],
                'span': (i, j)
            }
        else:
            # Nodo interno
            _, B, C, k = info
            left_child = self.build_parse_tree(parse_data, B, i, k)
            right_child = self.build_parse_tree(parse_data, C, k, j)
            
            return {
                'symbol': symbol,
                'type': 'nonterminal',
                'children': [left_child, right_child],
                'span': (i, j)
            }
    
    def print_parse_tree(self, tree: dict, indent: int = 0):
        """
        Imprime el árbol de parsing de forma legible.
        """
        if tree is None:
            return
        
        prefix = "  " * indent
        
        if tree['type'] == 'terminal':
            print(f"{prefix}{tree['symbol']} -> '{tree['value']}'")
        else:
            print(f"{prefix}{tree['symbol']}")
            for child in tree['children']:
                self.print_parse_tree(child, indent + 1)
    
    def save_parse_tree_graphviz(self, tree: dict, filename: str):
        """
        Guarda el árbol de parsing en formato DOT (Graphviz).
        """
        node_counter = [0]
        
        def get_node_id():
            node_counter[0] += 1
            return f"n{node_counter[0]}"
        
        def tree_to_dot(node, parent_id=None):
            if node is None:
                return ""
            
            node_id = get_node_id()
            
            if node['type'] == 'terminal':
                label = f"{node['symbol']}\\n'{node['value']}'"
                shape = "box"
            else:
                label = node['symbol']
                shape = "ellipse"
            
            dot = f'  {node_id} [label="{label}", shape={shape}];\n'
            
            if parent_id:
                dot += f'  {parent_id} -> {node_id};\n'
            
            if node['type'] == 'nonterminal':
                for child in node['children']:
                    dot += tree_to_dot(child, node_id)
            
            return dot
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("digraph ParseTree {\n")
                f.write("  rankdir=TB;\n")
                f.write("  node [fontname=\"Arial\"];\n")
                f.write(tree_to_dot(tree))
                f.write("}\n")
            print(f"✓ Árbol guardado en: {filename}")
            print(f"  Para visualizar: dot -Tpng {filename} -o parse_tree.png")
            return True
        except Exception as e:
            print(f"✗ Error al guardar árbol: {e}")
            return False


def list_grammar_files(directory="exercises"):
    """
    Lista todos los archivos .txt en el directorio especificado.
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            files.append(file)
    
    return sorted(files)


def select_grammar_file(directory="exercises"):
    """
    Muestra un menú para seleccionar un archivo de gramática.
    """
    files = list_grammar_files(directory)
    
    if not files:
        print(f"\n⚠ No se encontraron archivos .txt en '{directory}/'")
        return None
    
    print(f"\n{'='*70}")
    print(f"ARCHIVOS DE GRAMÁTICA DISPONIBLES EN '{directory}/'")
    print('='*70)
    
    for i, file in enumerate(files, 1):
        print(f"{i:2}. {file}")
    
    print(f" 0. Ingresar ruta manualmente")
    print('='*70)
    
    try:
        choice = input("\nSeleccione un archivo (0-{0}): ".format(len(files))).strip()
        
        if choice == '0':
            manual_path = input("Ingrese la ruta del archivo: ").strip()
            return manual_path
        
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return os.path.join(directory, files[idx])
        else:
            print("\n⚠ Opción inválida")
            return None
            
    except (ValueError, KeyboardInterrupt):
        return None


def main():
    """
    Programa principal - Menú interactivo.
    """
    converter = CNFConverter()
    parser = CYKParser()
    
    # Crear carpeta de output si no existe
    os.makedirs("output", exist_ok=True)
    
    print("\n" + "="*70)
    print("PROYECTO 2 - ALGORITMO CYK".center(70))
    print("Teoría de la Computación".center(70))
    print("="*70)
    
    while True:
        print("\n" + "="*70)
        print("MENÚ PRINCIPAL")
        print("="*70)
        print("1. Convertir gramática CFG a CNF")
        print("2. Cargar gramática CNF existente")
        print("3. Validar oracion con CYK")
        print("4. Ejecutar ejemplos de prueba")
        print("5. Salir")
        print("="*70)
        
        try:
            choice = input("\nSeleccione una opción (1-5): ").strip()
            
            if choice == '1':
                # Seleccionar archivo de entrada
                input_file = select_grammar_file("exercises")
                if not input_file:
                    continue
                
                # Generar nombre de salida automático
                base_name = os.path.basename(input_file)
                name_without_ext = os.path.splitext(base_name)[0]
                output_file = os.path.join("output", f"{name_without_ext}_cnf.txt")
                
                print(f"\n📁 Entrada:  {input_file}")
                print(f"📁 Salida:   {output_file}")
                
                if converter.full_conversion(input_file, output_file):
                    # Cargar automáticamente en el parser
                    parser.load_cnf_grammar(output_file)
            
            elif choice == '2':
                # Buscar primero en output/, luego en exercises/
                print("\n¿De dónde cargar la gramática CNF?")
                print("1. Carpeta output/ (archivos convertidos)")
                print("2. Carpeta exercises/ (archivos originales)")
                print("3. Ruta manual")
                
                sub_choice = input("\nSeleccione (1-3): ").strip()
                
                if sub_choice == '1':
                    cnf_file = select_grammar_file("output")
                elif sub_choice == '2':
                    cnf_file = select_grammar_file("exercises")
                elif sub_choice == '3':
                    cnf_file = input("Ruta del archivo CNF: ").strip()
                else:
                    print("\n⚠ Opción inválida")
                    continue
                
                if cnf_file:
                    parser.load_cnf_grammar(cnf_file)
            
            elif choice == '3':
                if not parser.grammar:
                    print("\n⚠ Primero debe cargar una gramática CNF (opción 1 o 2)")
                    continue
                
                print("\n" + "-"*70)
                sentence = input("Ingrese la oracion a validar: ").strip()
                
                if not sentence:
                    print("⚠ Oracion vacía")
                    continue
                
                accepted, elapsed, parse_data = parser.parse(sentence, verbose=True)
                
                if accepted and parse_data:
                    print("\n¿Desea ver el árbol de parsing? (s/n): ", end='')
                    if input().strip().lower() == 's':
                        tree = parser.build_parse_tree(parse_data)
                        print("\n" + "="*70)
                        print("ÁRBOL DE PARSING")
                        print("="*70)
                        parser.print_parse_tree(tree)
                        
                        print("\n¿Guardar árbol en formato DOT? (s/n): ", end='')
                        if input().strip().lower() == 's':
                            dot_file = input("Nombre del archivo (ej: tree.dot): ").strip()
                            parser.save_parse_tree_graphviz(tree, dot_file)
            
            elif choice == '4':
                if not parser.grammar:
                    print("\n⚠ Primero debe cargar una gramática CNF")
                    continue
                
                # Ejemplos de prueba
                test_sentences = [
                    "she eats a cake with a fork",
                    "the cat drinks the beer",
                    "he eats",
                    "she drinks juice",
                    "the dog eats meat with a spoon",
                    "fork eats the cat",  # Inválida
                    "she the eats",  # Inválida
                ]
                
                print("\n" + "="*70)
                print("PRUEBAS AUTOMÁTICAS")
                print("="*70)
                
                results = []
                for sentence in test_sentences:
                    print(f"\nProbando: '{sentence}'")
                    accepted, elapsed, _ = parser.parse(sentence, verbose=False)
                    results.append((sentence, accepted, elapsed))
                    status = "✓ ACEPTADA" if accepted else "✗ RECHAZADA"
                    print(f"  {status} ({elapsed*1000:.4f} ms)")
                
                print("\n" + "="*70)
                print("RESUMEN DE PRUEBAS")
                print("="*70)
                print(f"{'Oracion':<45} {'Estado':<12} {'Tiempo (ms)'}")
                print("-"*70)
                for sentence, accepted, elapsed in results:
                    status = "ACEPTADA" if accepted else "RECHAZADA"
                    print(f"{sentence:<45} {status:<12} {elapsed*1000:>10.4f}")
            
            elif choice == '5':
                print("\n¡Hasta luego!")
                break
            
            else:
                print("\n⚠ Opción inválida")
        
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
