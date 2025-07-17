"""
Controlador de Página Principal
==============================

Este módulo maneja la lógica de la página principal y dashboard del sistema,
coordinando la presentación de estadísticas y información general.

Funcionalidades principales:
- Dashboard principal con estadísticas
- Información del usuario actual
- Datos del sistema y grafos
- Coordinación entre diferentes módulos

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import render_template
from flask_login import current_user
from controllers.auth_controller import AuthController
from controllers.grafo_controller import GrafoController
from datetime import datetime

class HomeController:
    """
    Controlador que maneja las páginas principales y navegación del sistema.
    
    Coordina la presentación de información de diferentes módulos del sistema
    y proporciona una vista unificada del estado general de la aplicación.
    """
    
    @staticmethod
    def mostrar_bienvenida():
        """
        Muestra la página de bienvenida principal con estadísticas completas.
        
        Recopila información de diferentes partes del sistema:
        - Información del usuario actual
        - Estadísticas de usuarios del sistema
        - Estadísticas del grafo y rutas
        - Información general del sistema
        
        Returns:
            render_template: Dashboard principal con todas las estadísticas
        """
        # Obtener información detallada del usuario actual
        user_info = {
            'nombre': current_user.username,
            'email': current_user.email,
            'fecha_registro': current_user.created_at.strftime('%d/%m/%Y'),
            'activo': current_user.is_active
        }
        
        # Obtener estadísticas de usuarios del sistema
        stats_usuarios = AuthController.get_user_stats()
        
        # Obtener estadísticas del grafo y rutas
        stats_grafos = GrafoController.get_estadisticas_grafo()
        
        # Información general del sistema
        sistema_info = {
            'version': '1.0.0',
            'fecha_actual': datetime.now().strftime('%d/%m/%Y'),
            'hora_actual': datetime.now().strftime('%H:%M:%S')
        }
        
        return render_template(
            'user/dashboard.html', 
            user_info=user_info,
            stats_usuarios=stats_usuarios,
            stats_grafos=stats_grafos,
            sistema_info=sistema_info
        )
    
    @staticmethod
    def get_dashboard_data():
        """
        Obtiene datos consolidados para el dashboard desde múltiples fuentes.
        
        Esta función centraliza la recopilación de datos para APIs o
        actualizaciones dinámicas del dashboard.
        
        Returns:
            dict: Diccionario con todas las estadísticas del sistema
        """
        return {
            'usuarios': AuthController.get_user_stats(),    # Estadísticas de usuarios
            'grafos': GrafoController.get_estadisticas_grafo(),  # Estadísticas del grafo
            'sistema': {
                'version': '1.0.0',
                'uptime': 'Activo',
                'ultima_actualizacion': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
        }
