"""
Modelos de Datos
===============

Este módulo importa todos los modelos de la aplicación para que estén disponibles
cuando se importe el paquete models. Esto facilita la gestión de imports y
asegura que SQLAlchemy reconozca todos los modelos.

Modelos incluidos:
- User: Gestión de usuarios y autenticación
- Ciudad: Representación de ciudades en el grafo
- Ruta: Conexiones entre ciudades con sus costos
- Provincia: Agrupación territorial de ciudades

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from .user import User           # Modelo de usuarios del sistema
from .ciudad import Ciudad       # Modelo de ciudades (nodos del grafo)
from .ruta import Ruta          # Modelo de rutas (aristas del grafo)
from .provincia import Provincia # Modelo de provincias (agrupación territorial)

__all__ = [
    'User',
    'Ciudad',
    'Ruta',
    'Provincia'
]