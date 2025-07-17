"""
Configuración de la Aplicación Flask
===================================

Este módulo contiene la configuración principal de la aplicación,
incluyendo parámetros de base de datos, seguridad y variables de entorno.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

# Importa el módulo os para acceder a las variables de entorno del sistema
import os

# Importa la función load_dotenv para cargar las variables desde el archivo .env
from dotenv import load_dotenv

# Carga automáticamente las variables definidas en el archivo .env al entorno del sistema
load_dotenv()

class Config:
    """
    Clase de configuración que centraliza todos los parámetros de la aplicación.
    Utiliza variables de entorno para mayor seguridad y flexibilidad.
    """
    
    # Configuración de la base de datos MySQL
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'          # Servidor de base de datos
    DB_NAME = os.environ.get('DB_NAME') or 'proyecto_final'     # Nombre de la base de datos
    DB_USER = os.environ.get('DB_USER') or 'root'               # Usuario de MySQL
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''           # Contraseña de MySQL
    DB_PORT = os.environ.get('DB_PORT') or '3306'               # Puerto de MySQL
    
    # Construye la URI de conexión a MySQL usando las variables de entorno cargadas
    # Formato: mysql+pymysql://usuario:contraseña@host:puerto/nombre_base
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Desactiva el rastreo de modificaciones de objetos (recomendado para rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para proteger contra ataques CSRF y firmar cookies de sesión
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-super-segura'
