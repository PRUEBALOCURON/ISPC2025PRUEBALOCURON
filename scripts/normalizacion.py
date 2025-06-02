"""
MÓDULO PROFESIONAL DE NORMALIZACIÓN
----------------------------------
Características:
- Validación de tipos de datos
- Manejo de casos especiales
- Generación de reportes estructurados
- Registro de metadatos
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Union

class Normalizador:
    VERSION = "1.0.0"
    
    @classmethod
    def get_info(cls) -> Dict[str, str]:
        """Retorna metadatos del normalizador"""
        return {
            "version": cls.VERSION,
            "autor": "Tu Nombre",
            "fecha_actualizacion": "2024-03-15"
        }

    @staticmethod
    def normalizar(datos: List[Union[float, int]]) -> List[float]:
        """
        Normaliza datos usando Min-Max Scaling
        
        Args:
            datos: Lista de valores numéricos
            
        Returns:
            Lista de valores normalizados [0-1]
            
        Raises:
            TypeError: Si los datos no son una lista
            ValueError: Si contiene valores no numéricos
        """
        # Validación de tipo
        if not isinstance(datos, list):
            raise TypeError("Los datos deben ser una lista")
            
        # Casos especiales
        if not datos:
            return []
            
        if len(datos) == 1:
            return [0.5]
            
        # Validación de valores numéricos
        try:
            minimo = min(datos)
            maximo = max(datos)
        except TypeError:
            raise ValueError("Todos los elementos deben ser numéricos")
            
        # Normalización
        rango = maximo - minimo
        if rango == 0:
            return [0.0] * len(datos)
            
        return [(x - minimo) / rango for x in datos]

def generar_reporte(datos_originales: List[float]) -> Dict:
    """Genera un reporte estructurado con metadatos"""
    normalizados = Normalizador.normalizar(datos_originales)
    
    return {
        "meta": {
            "fecha_generacion": datetime.now().isoformat(),
            **Normalizador.get_info()
        },
        "datos": {
            "originales": datos_originales,
            "normalizados": normalizados,
            "estadisticas": {
                "min": min(datos_originales),
                "max": max(datos_originales),
                "rango": max(datos_originales) - min(datos_originales)
            }
        }
    }

def guardar_reporte(reporte: Dict, directorio: str = "data") -> str:
    """Guarda el reporte en formato JSON"""
    os.makedirs(directorio, exist_ok=True)
    ruta_archivo = os.path.join(directorio, "reporte_normalizacion.json")
    
    with open(ruta_archivo, 'w') as f:
        json.dump(reporte, f, indent=4)
        
    return ruta_archivo

def main():
    try:
        # 1. Datos de ejemplo
        pesos_manzanas = [50.0, 150.0, 300.0]
        
        # 2. Generar reporte
        reporte = generar_reporte(pesos_manzanas)
        
        # 3. Guardar resultados
        ruta = guardar_reporte(reporte)
        
        # 4. Mostrar resultados
        print("✅ Normalización completada con éxito")
        print(f"📊 Reporte generado en: {os.path.abspath(ruta)}")
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())