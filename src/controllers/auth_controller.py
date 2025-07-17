"""
Controlador de Autenticación
===========================

Este módulo maneja toda la lógica relacionada con autenticación de usuarios,
incluyendo login, registro, validaciones y estadísticas de usuarios.

Funcionalidades principales:
- Inicio de sesión de usuarios
- Registro de nuevos usuarios
- Validaciones de datos de entrada
- Estadísticas de usuarios del sistema

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from models import User
from extensions import db
from datetime import datetime

class AuthController:
    """
    Controlador que maneja la autenticación y gestión de usuarios.
    
    Implementa el patrón MVC separando la lógica de autenticación
    de la presentación y proporcionando validaciones robustas.
    """
    
    @staticmethod
    def login():
        """
        Maneja el proceso de inicio de sesión de usuarios.
        
        Proceso:
        1. Verifica si el usuario ya está autenticado
        2. Valida credenciales proporcionadas
        3. Busca usuario por username o email
        4. Verifica contraseña usando hash seguro
        5. Inicia sesión y redirige según corresponda
        
        Returns:
            render_template: Página de login o redirección al dashboard
        """
        # Redirigir usuarios ya autenticados
        if current_user.is_authenticated:
            return redirect(url_for('home.home'))
        
        if request.method == 'POST':
            # Obtener datos del formulario
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Validación básica de campos obligatorios
            if not username or not password:
                flash('Por favor completa todos los campos.', 'error')
                return render_template('auth/login.html')
            
            # Buscar usuario por username o email (flexibilidad de login)
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            # Verificar credenciales usando hash seguro
            if user and user.check_password(password):
                # Iniciar sesión exitosa
                login_user(user)
                flash(f'¡Bienvenido {user.username}!', 'success')
                
                # Redirigir a la página solicitada o al home
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home.home'))
            else:
                # Credenciales incorrectas
                flash('Usuario o contraseña incorrectos.', 'error')
        
        return render_template('auth/login.html')
    
    @staticmethod
    def register():
        """
        Maneja el proceso de registro de nuevos usuarios.
        
        Proceso:
        1. Verifica que el usuario no esté ya autenticado
        2. Valida todos los datos del formulario
        3. Verifica unicidad de username y email
        4. Crea el usuario con contraseña hasheada
        5. Guarda en base de datos y redirige al login
        
        Returns:
            render_template: Página de registro o redirección al login
        """
        # Redirigir usuarios ya autenticados
        if current_user.is_authenticated:
            return redirect(url_for('home.home'))
        
        if request.method == 'POST':
            # Obtener todos los datos del formulario
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Ejecutar validaciones completas
            validation_result = AuthController._validate_registration(
                username, email, password, confirm_password
            )
            
            # Si hay errores de validación, mostrarlos
            if validation_result != True:
                flash(validation_result, 'error')
                return render_template('auth/register.html')
            
            # Intentar crear el nuevo usuario
            try:
                # Crear instancia del usuario
                user = User(username=username, email=email)
                user.set_password(password)  # Hash seguro de la contraseña
                
                # Guardar en base de datos
                db.session.add(user)
                db.session.commit()
                
                flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
                return redirect(url_for('auth.login'))
                
            except Exception as e:
                # Manejar errores de base de datos
                db.session.rollback()
                flash('Error al registrar el usuario. Inténtalo de nuevo.', 'error')
                print(f"Error en registro: {e}")
        
        return render_template('auth/register.html')
    
    @staticmethod
    def _validate_registration(username, email, password, confirm_password):
        """
        Valida exhaustivamente todos los datos de registro.
        
        Validaciones incluidas:
        - Campos obligatorios
        - Longitud de campos
        - Formato de email
        - Fortaleza de contraseña
        - Caracteres permitidos
        - Unicidad de username y email
        
        Args:
            username (str): Nombre de usuario propuesto
            email (str): Email del usuario
            password (str): Contraseña en texto plano
            confirm_password (str): Confirmación de contraseña
            
        Returns:
            str|bool: Mensaje de error o True si todo es válido
        """
        # Validar que todos los campos estén presentes
        if not username or not email or not password or not confirm_password:
            return 'Por favor completa todos los campos.'
        
        # Validar longitud mínima del username
        if len(username) < 3:
            return 'El nombre de usuario debe tener al menos 3 caracteres.'
        
        # Validar longitud máxima del username
        if len(username) > 80:
            return 'El nombre de usuario no puede tener más de 80 caracteres.'
        
        # Validar formato del email usando regex
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return 'Por favor ingresa un email válido.'
        
        # Validar longitud máxima del email
        if len(email) > 120:
            return 'El email no puede tener más de 120 caracteres.'
        
        # Validar que las contraseñas coincidan
        if password != confirm_password:
            return 'Las contraseñas no coinciden.'
        
        # Validar longitud mínima de contraseña
        if len(password) < 6:
            return 'La contraseña debe tener al menos 6 caracteres.'
        
        # Validar longitud máxima de contraseña
        if len(password) > 128:
            return 'La contraseña no puede tener más de 128 caracteres.'
        
        # Validar caracteres permitidos en username (solo alfanuméricos y guiones bajos)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return 'El nombre de usuario solo puede contener letras, números y guiones bajos.'
        
        # Verificar unicidad del username (case insensitive)
        existing_user = User.query.filter(
            db.func.lower(User.username) == username.lower()
        ).first()
        if existing_user:
            return f'El nombre de usuario "{username}" ya está en uso. Por favor elige otro.'
        
        # Verificar unicidad del email (case insensitive)
        existing_email = User.query.filter(
            db.func.lower(User.email) == email.lower()
        ).first()
        if existing_email:
            return f'El email "{email}" ya está registrado. ¿Ya tienes una cuenta?'
        
        # Todas las validaciones pasaron
        return True
    
    @staticmethod
    def get_user_stats():
        """
        Obtiene estadísticas de usuarios para mostrar en dashboards administrativos.
        
        Calcula:
        - Total de usuarios registrados
        - Usuarios activos
        - Usuarios registrados en el mes actual
        
        Returns:
            dict: Diccionario con las estadísticas de usuarios
        """
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        
        # Usuarios registrados en el mes actual
        recent_users = User.query.filter(
            User.created_at >= datetime.now().replace(day=1)
        ).count()
        
        return {
            'total': total_users,
            'active': active_users,
            'recent': recent_users
        }
