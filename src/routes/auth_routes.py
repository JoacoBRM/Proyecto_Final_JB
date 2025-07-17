"""
Rutas de Autenticación
=====================

Este módulo define las rutas relacionadas con la autenticación de usuarios.
Utiliza blueprints de Flask para organizar las rutas de forma modular.

Rutas incluidas:
- /login: Inicio de sesión de usuarios
- /register: Registro de nuevos usuarios  
- /logout: Cierre de sesión

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user, login_required
from controllers.auth_controller import AuthController

# Crear blueprint para rutas de autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para inicio de sesión de usuarios.
    
    Acepta métodos GET (mostrar formulario) y POST (procesar login).
    Delega la lógica al AuthController siguiendo el patrón MVC.
    
    Returns:
        Response: Formulario de login o redirección según el resultado
    """
    return AuthController.login()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta para registro de nuevos usuarios.
    
    Acepta métodos GET (mostrar formulario) y POST (procesar registro).
    Incluye validaciones completas de datos de entrada.
    
    Returns:
        Response: Formulario de registro o redirección según el resultado
    """
    return AuthController.register()

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Ruta para cerrar sesión de usuarios autenticados.
    
    Requiere que el usuario esté logueado (@login_required).
    Cierra la sesión actual y redirige al login.
    
    Returns:
        Response: Redirección al formulario de login con mensaje
    """
    logout_user()  # Cerrar sesión usando Flask-Login
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))
