"""
Módulo de pruebas automáticas para el parser CYK
Carga casos de prueba desde archivos externos y ejecuta validaciones
"""

import os
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class TestCase:
    """Representa un caso de prueba individual"""
    sentence: str
    expected: bool  # True = accept, False = reject
    line_number: int


class TestRunner:
    """
    Ejecuta casos de prueba para el parser CYK
    """
    
    def __init__(self, parser):
        self.parser = parser
        self.test_cases_dir = "test_cases"
    
    def load_test_cases(self, filename: str) -> List[TestCase]:
        """
        Carga casos de prueba desde un archivo.
        Formato: <oración> | <accept/reject>
        """
        filepath = os.path.join(self.test_cases_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ Archivo de pruebas no encontrado: {filepath}")
            return []
        
        test_cases = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Ignorar comentarios y líneas vacías
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parsear formato: sentence | expected
                    if '|' not in line:
                        continue
                    
                    parts = line.split('|')
                    if len(parts) != 2:
                        continue
                    
                    sentence = parts[0].strip()
                    expected_str = parts[1].strip().lower()
                    
                    # Convertir expected a booleano
                    if expected_str == 'accept':
                        expected = True
                    elif expected_str == 'reject':
                        expected = False
                    else:
                        print(f"⚠ Línea {line_num}: Valor esperado inválido '{expected_str}' (debe ser 'accept' o 'reject')")
                        continue
                    
                    test_cases.append(TestCase(sentence, expected, line_num))
            
            return test_cases
            
        except Exception as e:
            print(f"✗ Error al cargar casos de prueba: {e}")
            return []
    
    def list_test_files(self) -> List[str]:
        """
        Lista todos los archivos de prueba disponibles.
        """
        if not os.path.exists(self.test_cases_dir):
            return []
        
        files = []
        for file in os.listdir(self.test_cases_dir):
            if file.endswith('_tests.txt'):
                files.append(file)
        
        return sorted(files)
    
    def run_test_suite(self, test_file: str, verbose: bool = False) -> Dict:
        """
        Ejecuta una suite completa de pruebas.
        
        Retorna un diccionario con estadísticas:
        - total: número total de pruebas
        - passed: pruebas exitosas
        - failed: pruebas fallidas
        - results: lista de resultados detallados
        """
        test_cases = self.load_test_cases(test_file)
        
        if not test_cases:
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'results': []
            }
        
        print(f"\n{'='*70}")
        print(f"EJECUTANDO SUITE DE PRUEBAS: {test_file}")
        print('='*70)
        print(f"Total de casos: {len(test_cases)}")
        
        results = []
        passed = 0
        failed = 0
        
        for i, test in enumerate(test_cases, 1):
            if verbose:
                print(f"\n[{i}/{len(test_cases)}] Probando: '{test.sentence}'")
            
            try:
                accepted, elapsed, _ = self.parser.parse(test.sentence, verbose=False)
                
                # Verificar si el resultado coincide con lo esperado
                test_passed = (accepted == test.expected)
                
                if test_passed:
                    passed += 1
                    status = "✓ PASS"
                    status_color = "\033[92m"  # Verde
                else:
                    failed += 1
                    status = "✗ FAIL"
                    status_color = "\033[91m"  # Rojo
                
                reset_color = "\033[0m"
                
                result = {
                    'sentence': test.sentence,
                    'expected': 'ACCEPT' if test.expected else 'REJECT',
                    'actual': 'ACCEPT' if accepted else 'REJECT',
                    'passed': test_passed,
                    'time_ms': elapsed * 1000,
                    'line': test.line_number
                }
                
                results.append(result)
                
                if verbose or not test_passed:
                    print(f"  Esperado: {result['expected']:8} | Obtenido: {result['actual']:8} | {status_color}{status}{reset_color} | {elapsed*1000:.2f}ms")
            
            except Exception as e:
                failed += 1
                print(f"  ✗ ERROR: {e}")
                results.append({
                    'sentence': test.sentence,
                    'expected': 'ACCEPT' if test.expected else 'REJECT',
                    'actual': 'ERROR',
                    'passed': False,
                    'time_ms': 0,
                    'line': test.line_number,
                    'error': str(e)
                })
        
        return {
            'total': len(test_cases),
            'passed': passed,
            'failed': failed,
            'results': results
        }
    
    def print_summary(self, stats: Dict):
        """
        Imprime un resumen de los resultados de las pruebas.
        """
        print(f"\n{'='*70}")
        print("RESUMEN DE PRUEBAS")
        print('='*70)
        
        total = stats['total']
        passed = stats['passed']
        failed = stats['failed']
        
        if total == 0:
            print("No se ejecutaron pruebas")
            return
        
        success_rate = (passed / total) * 100
        
        # Colores
        green = "\033[92m"
        red = "\033[91m"
        yellow = "\033[93m"
        reset = "\033[0m"
        
        print(f"Total de pruebas:     {total}")
        print(f"{green}Pruebas exitosas:     {passed}{reset}")
        print(f"{red}Pruebas fallidas:     {failed}{reset}")
        print(f"Tasa de éxito:        {success_rate:.1f}%")
        
        # Mostrar pruebas fallidas en detalle
        if failed > 0:
            print(f"\n{red}PRUEBAS FALLIDAS:{reset}")
            print("-"*70)
            print(f"{'Oración':<35} {'Esperado':<10} {'Obtenido':<10} {'Línea'}")
            print("-"*70)
            
            for result in stats['results']:
                if not result['passed']:
                    sentence = result['sentence']
                    if len(sentence) > 32:
                        sentence = sentence[:29] + "..."
                    print(f"{sentence:<35} {result['expected']:<10} {result['actual']:<10} {result['line']}")
        
        # Tiempo promedio
        if stats['results']:
            avg_time = sum(r['time_ms'] for r in stats['results']) / len(stats['results'])
            print(f"\nTiempo promedio:      {avg_time:.2f} ms")
        
        print('='*70)
    
    def export_results(self, stats: Dict, output_file: str = "output/test_results.txt"):
        """
        Exporta los resultados de las pruebas a un archivo.
        """
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("RESULTADOS DE PRUEBAS CYK\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Total de pruebas: {stats['total']}\n")
                f.write(f"Exitosas: {stats['passed']}\n")
                f.write(f"Fallidas: {stats['failed']}\n")
                f.write(f"Tasa de éxito: {(stats['passed']/stats['total']*100):.1f}%\n\n")
                
                f.write("="*70 + "\n")
                f.write("RESULTADOS DETALLADOS\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"{'Oración':<40} {'Esperado':<10} {'Obtenido':<10} {'Estado':<8} {'Tiempo(ms)'}\n")
                f.write("-"*70 + "\n")
                
                for result in stats['results']:
                    status = "PASS" if result['passed'] else "FAIL"
                    f.write(f"{result['sentence']:<40} {result['expected']:<10} {result['actual']:<10} {status:<8} {result['time_ms']:>10.2f}\n")
            
            print(f"\n✓ Resultados exportados a: {output_file}")
            return True
            
        except Exception as e:
            print(f"✗ Error al exportar resultados: {e}")
            return False


def select_test_file(test_runner: TestRunner) -> Optional[str]:
    """
    Muestra un menú para seleccionar un archivo de pruebas.
    """
    files = test_runner.list_test_files()
    
    if not files:
        print(f"\n⚠ No se encontraron archivos de prueba en '{test_runner.test_cases_dir}/'")
        return None
    
    print(f"\n{'='*70}")
    print(f"ARCHIVOS DE PRUEBA DISPONIBLES")
    print('='*70)
    
    for i, file in enumerate(files, 1):
        # Extraer nombre descriptivo del archivo
        name = file.replace('_tests.txt', '').replace('_', ' ').title()
        print(f"{i:2}. {name:<35} ({file})")
    
    print(f" 0. Cancelar")
    print('='*70)
    
    try:
        choice = input(f"\nSeleccione un archivo (0-{len(files)}): ").strip()
        
        if choice == '0':
            return None
        
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
        else:
            print("\n⚠ Opción inválida")
            return None
            
    except (ValueError, KeyboardInterrupt):
        return None
