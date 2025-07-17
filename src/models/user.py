"""
Modelo de Usuario
================

Este módulo define el modelo de datos para los usuarios del sistema,
incluyendo autenticación, validación y métodos de utilidad.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

class User(UserMixin, db.Model):
    """
    Modelo de usuario que maneja la autenticación y datos de usuarios.
    
    Hereda de UserMixin para integración con Flask-Login y db.Model para SQLAlchemy.
    Incluye validaciones de datos y métodos para manejo seguro de contraseñas.
    """
    
    __tablename__ = 'users'
    
    # Campos de la tabla users
    id = db.Column(db.Integer, primary_key=True)                    # ID único del usuario
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)  # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)    # Email único
    password_hash = db.Column(db.String(255), nullable=False)       # Contraseña hasheada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)    # Fecha de creación
    is_active = db.Column(db.Boolean, default=True)                 # Estado activo del usuario
    
    def set_password(self, password):
        """
        Establece la contraseña del usuario de forma segura usando hash.
        
        Args:
            password (str): Contraseña en texto plano
            
        Raises:
            ValueError: Si la contraseña es demasiado corta
        """
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada es correcta.
        
        Args:
            password (str): Contraseña en texto plano a verificar
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario
        """
        return check_password_hash(self.password_hash, password)
    
    def validate_username(self, username):
        """
        Valida el formato y unicidad del nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a validar
            
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        # Validar longitud mínima
        if not username or len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        
        # Validar longitud máxima
        if len(username) > 80:
            return False, "El nombre de usuario no puede tener más de 80 caracteres"
        
        # Validar formato (solo letras, números y guiones bajos)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
        
        # Verificar unicidad (case insensitive)
        existing = User.query.filter(
            db.func.lower(User.username) == username.lower(),
            User.id != self.id  # Excluir el usuario actual en caso de actualización
        ).first()
        
        if existing:
            return False, f"El nombre de usuario '{username}' ya está en uso"
        
        return True, "Válido"
    
    def validate_email(self, email):
        """
        Valida el formato y unicidad del email.
        
        Args:
            email (str): Email a validar
            
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        # Patrón regex para validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Validar que no esté vacío
        if not email:
            return False, "El email es obligatorio"
        
        # Validar longitud máxima
        if len(email) > 120:
            return False, "El email no puede tener más de 120 caracteres"
        
        # Validar formato usando regex
        if not re.match(email_pattern, email):
            return False, "Por favor ingresa un email válido"
        
        # Verificar unicidad (case insensitive)
        existing = User.query.filter(
            db.func.lower(User.email) == email.lower(),
            User.id != self.id  # Excluir el usuario actual en caso de actualización
        ).first()
        
        if existing:
            return False, f"El email '{email}' ya está registrado"
        
        return True, "Válido"
    
    @classmethod
    def username_exists(cls, username):
        """
        Verifica si un username ya existe en la base de datos.
        
        Args:
            username (str): Nombre de usuario a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return cls.query.filter(
            db.func.lower(cls.username) == username.lower()
        ).first() is not None
    
    @classmethod
    def email_exists(cls, email):
        """
        Verifica si un email ya existe en la base de datos.
        
        Args:
            email (str): Email a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return cls.query.filter(
            db.func.lower(cls.email) == email.lower()
        ).first() is not None
    
    def __repr__(self):
        """Representación string del objeto User para debugging."""
        return f'<User {self.username}>'
