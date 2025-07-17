"""
Rutas de Página Principal
========================

Este módulo define las rutas principales de la aplicación,
incluyendo la página de inicio y el dashboard principal.

Rutas incluidas:
- /: Página de entrada (redirige según autenticación)
- /home: Dashboard principal para usuarios autenticados

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from controllers import HomeController

# Crear blueprint para rutas principales
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """
    Ruta raíz de la aplicación.
    
    Actúa como punto de entrada principal y redirige a los usuarios
    según su estado de autenticación.
    
    Returns:
        Response: Redirección al login o al dashboard según autenticación
    """
    # Redirigir al login si no está autenticado
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Redirigir al dashboard si ya está autenticado
    return redirect(url_for('home.home'))

@home_bp.route('/home')
@login_required
def home():
    """
    Dashboard principal para usuarios autenticados.
    
    Muestra estadísticas del sistema, información del usuario
    y accesos rápidos a las funcionalidades principales.
    
    Returns:
        Response: Página de dashboard con estadísticas completas
    """
    return HomeController.mostrar_bienvenida()