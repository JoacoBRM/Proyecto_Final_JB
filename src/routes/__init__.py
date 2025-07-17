"""
Rutas de la Aplicación
=====================

Este módulo importa y registra todos los blueprints (rutas) de la aplicación Flask.
Los blueprints organizan las rutas en módulos lógicos según su funcionalidad.

Blueprints incluidos:
- auth_bp: Rutas de autenticación (login, register, logout)
- home_bp: Rutas de página principal y dashboard
- starter_bp: Rutas de grafos y cálculo de rutas
- admin_bp: Rutas administrativas (CRUD de datos)

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from .home_routes import home_bp        # Rutas de página principal
from .grafos_routes import starter_bp   # Rutas de grafos y algoritmos
from .auth_routes import auth_bp        # Rutas de autenticación
from .admin_routes import admin_bp      # Rutas administrativas

def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación Flask.
    
    El orden de registro puede afectar la precedencia de las rutas,
    por lo que se registran en orden de importancia.
    
    Args:
        app (Flask): Instancia de la aplicación Flask
    """
    app.register_blueprint(auth_bp)     # Autenticación (prioritario)
    app.register_blueprint(home_bp)     # Página principal
    app.register_blueprint(starter_bp)  # Funcionalidad de grafos
    app.register_blueprint(admin_bp)    # Administración