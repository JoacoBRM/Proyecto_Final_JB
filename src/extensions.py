"""
Extensiones de Flask
===================

Este módulo inicializa y configura las extensiones utilizadas en la aplicación,
como SQLAlchemy para la base de datos y Flask-Login para autenticación.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

# Importa las extensiones necesarias de Flask
from flask_sqlalchemy import SQLAlchemy  # ORM para manejo de base de datos
from flask_login import LoginManager     # Sistema de autenticación de usuarios

# Crear instancias globales de las extensiones
# Estas instancias serán compartidas por toda la aplicación
db = SQLAlchemy()                        # Instancia del ORM para base de datos
login_manager = LoginManager()           # Instancia del gestor de autenticación

# Configuración del sistema de autenticación
login_manager.login_view = 'auth.login'  # Ruta a la que redirigir usuarios no autenticados
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'  # Categoría del mensaje (para estilos CSS)

@login_manager.user_loader
def load_user(user_id):
    """
    Función callback requerida por Flask-Login para cargar un usuario.
    Se llama automáticamente cuando Flask necesita obtener el usuario actual.
    
    Args:
        user_id (str): ID del usuario como string
        
    Returns:
        User: Objeto usuario correspondiente al ID o None si no existe
    """
    from models.user import User  # Importación tardía para evitar imports circulares
    return User.query.get(int(user_id))
