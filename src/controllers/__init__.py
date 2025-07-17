"""
Controladores de la Aplicación
=============================

Este módulo importa todos los controladores de la aplicación para facilitar
su uso desde otros módulos. Los controladores implementan la lógica de negocio
del patrón MVC.

Controladores incluidos:
- AuthController: Manejo de autenticación y autorización
- GrafoController: Lógica de grafos y algoritmo de Dijkstra
- HomeController: Páginas principales y navegación
- AdminController: Funcionalidades administrativas

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from .auth_controller import AuthController      # Controlador de autenticación
from .grafo_controller import GrafoController    # Controlador de grafos y rutas
from .home_controller import HomeController      # Controlador de páginas principales
from .admin_controller import AdminController    # Controlador administrativo

# Exportar todos los controllers
__all__ = [
    'AuthController',
    'GrafoController', 
    'HomeController',
    'AdminController'
]
