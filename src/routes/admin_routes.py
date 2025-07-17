"""
Rutas Administrativas
====================

Este módulo define todas las rutas para la administración del sistema,
incluyendo CRUD completo de provincias, ciudades y rutas.

Funcionalidades incluidas:
- Gestión de provincias (crear, editar, eliminar, listar)
- Gestión de ciudades (crear, editar, eliminar, listar)
- Gestión de rutas (crear, editar, eliminar, listar)
- APIs para obtener datos dinámicos

Todas las rutas requieren autenticación y tienen el prefijo /admin

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import Blueprint
from controllers import AdminController

# Crear blueprint para rutas administrativas con prefijo URL
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ===== RUTAS PARA GESTIÓN DE PROVINCIAS =====
# Listar todas las provincias
admin_bp.route('/provincias', methods=['GET'])(AdminController.listar_provincias)

# Crear nueva provincia
admin_bp.route('/provincias/crear', methods=['POST'])(AdminController.crear_provincia)

# Editar provincia existente
admin_bp.route('/provincias/<int:provincia_id>/editar', methods=['GET', 'POST'])(AdminController.editar_provincia)

# Eliminar provincia
admin_bp.route('/provincias/<int:provincia_id>/eliminar', methods=['POST'])(AdminController.eliminar_provincia)


# ===== RUTAS PARA GESTIÓN DE CIUDADES =====
# Listar todas las ciudades
admin_bp.route('/ciudades', methods=['GET'])(AdminController.listar_ciudades)

# Crear nueva ciudad con sus conexiones
admin_bp.route('/ciudades/crear', methods=['POST'])(AdminController.crear_ciudad)

# Editar ciudad existente
admin_bp.route('/ciudades/<int:ciudad_id>/editar', methods=['GET', 'POST'])(AdminController.editar_ciudad)

# Eliminar ciudad
admin_bp.route('/ciudades/<int:ciudad_id>/eliminar', methods=['POST'])(AdminController.eliminar_ciudad)


# ===== RUTAS PARA GESTIÓN DE RUTAS =====
# Listar todas las rutas del sistema
admin_bp.route('/rutas', methods=['GET'])(AdminController.listar_rutas)

# Crear nueva ruta directa entre ciudades
admin_bp.route('/rutas/crear', methods=['POST'])(AdminController.crear_ruta_directa)

# Editar ruta existente
admin_bp.route('/rutas/editar', methods=['POST'])(AdminController.editar_ruta_directa)

# Eliminar ruta específica
admin_bp.route('/rutas/eliminar', methods=['POST'])(AdminController.eliminar_ruta_directa)

# Agregar ruta a una ciudad existente
admin_bp.route('/rutas/agregar', methods=['POST'])(AdminController.agregar_ruta_ciudad)

# Eliminar conexión específica entre ciudades
admin_bp.route('/rutas/eliminar-conexion', methods=['POST'])(AdminController.eliminar_ruta)

