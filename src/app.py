"""
Sistema de Rutas con Grafos - Aplicación Principal
=================================================

Este módulo contiene la configuración principal de la aplicación Flask
que implementa un sistema de cálculo de rutas óptimas entre ciudades
utilizando el algoritmo de Dijkstra.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import Flask
from config import Config
from extensions import db, login_manager
from models.user import User
# Importar todos los modelos para que SQLAlchemy los reconozca
from models import *

# Importamos las rutas desde la carpeta routes
from routes import register_blueprints

# Crear la instancia principal de la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde el archivo config.py
app.config.from_object(Config)

# Inicializar las extensiones de Flask
db.init_app(app)              # Base de datos SQLAlchemy
login_manager.init_app(app)   # Sistema de autenticación

@login_manager.user_loader
def load_user(user_id):
    """
    Función requerida por Flask-Login para cargar un usuario desde su ID.
    
    Args:
        user_id (str): ID del usuario como string
        
    Returns:
        User: Objeto usuario correspondiente al ID o None si no existe
    """
    return User.query.get(int(user_id))
    
# Registrar todos los blueprints (rutas) de la aplicación
register_blueprints(app)

if __name__ == '__main__':
    """
    Ejecutar la aplicación Flask en modo desarrollo.
    - debug=True: Permite recarga automática y debugging
    - host="0.0.0.0": Acepta conexiones desde cualquier IP
    - port=4000: Ejecuta en el puerto 4000
    """
    app.run(debug=True, host="0.0.0.0", port=4000)
