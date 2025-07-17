"""
Controlador Administrativo
=========================

Este módulo maneja todas las funcionalidades administrativas del sistema,
incluyendo gestión de provincias, ciudades y rutas.

Funcionalidades principales:
- CRUD completo de provincias
- CRUD completo de ciudades  
- CRUD completo de rutas
- Validaciones de datos administrativos
- Gestión de relaciones entre entidades

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from extensions import db
from models import Provincia, Ciudad, Ruta

class AdminController:
    """
    Controlador que maneja todas las operaciones administrativas del sistema.
    
    Proporciona interfaces CRUD para todas las entidades principales
    y mantiene la integridad de los datos del sistema.
    """
    
    @staticmethod
    @login_required
    def listar_provincias():
        """
        Lista todas las provincias del sistema.
        
        Returns:
            render_template: Página con lista de todas las provincias
        """
        provincias = Provincia.obtener_todas()
        return render_template('admin/provincias.html', provincias=provincias)
    
    @staticmethod
    @login_required
    def crear_provincia():
        """
        Crea una nueva provincia en el sistema.
        
        Proceso:
        1. Valida datos de entrada
        2. Verifica unicidad del nombre
        3. Crea y guarda la provincia
        4. Redirige con mensaje de confirmación
        
        Returns:
            redirect: Redirección a la lista de provincias con mensaje
        """
        if request.method == 'POST':
            # Obtener y limpiar el nombre de la provincia
            nombre = request.form.get('nombre', '').strip()
            
            # Validación básica de campo obligatorio
            if not nombre:
                flash('El nombre de la provincia es obligatorio', 'error')
                return redirect(url_for('admin.listar_provincias'))
            
            # Crear objeto temporal para ejecutar validaciones del modelo
            nueva_provincia = Provincia(nombre=nombre)
            es_valido, mensaje = nueva_provincia.validate_name()
            
            # Verificar si pasó todas las validaciones
            if not es_valido:
                flash(mensaje, 'error')
                return redirect(url_for('admin.listar_provincias'))
            
            # Intentar guardar en base de datos
            try:
                db.session.add(nueva_provincia)
                db.session.commit()
                flash('Provincia creada exitosamente', 'success')
            except Exception as e:
                # Manejar errores de base de datos
                db.session.rollback()
                flash('Error al crear la provincia', 'error')
                print(f"Error creando provincia: {e}")
        
        return redirect(url_for('admin.listar_provincias'))
    
    @staticmethod
    @login_required
    def editar_provincia(provincia_id):
        """
        Edita una provincia existente.
        
        Args:
            provincia_id (int): ID de la provincia a editar
            
        Returns:
            render_template: Página de edición o redirección con mensaje
        """
        provincia = Provincia.query.get_or_404(provincia_id)
        
        if request.method == 'POST':
            # Obtener y limpiar el nombre del formulario
            nombre = request.form.get('nombre', '').strip()
            
            # Validación básica de campo obligatorio
            if not nombre:
                flash('El nombre de la provincia es obligatorio', 'error')
                return render_template('admin/editar_provincia.html', provincia=provincia)
            
            # Actualizar nombre temporalmente para ejecutar validaciones
            nombre_original = provincia.nombre
            provincia.nombre = nombre
            es_valido, mensaje = provincia.validate_name()
            
            # Verificar si pasó todas las validaciones
            if not es_valido:
                provincia.nombre = nombre_original  # Restaurar nombre original
                flash(mensaje, 'error')
                return render_template('admin/editar_provincia.html', provincia=provincia)
            
            # Intentar guardar cambios en base de datos
            try:
                db.session.commit()
                flash('Provincia actualizada exitosamente', 'success')
                return redirect(url_for('admin.listar_provincias'))
            except Exception as e:
                # Manejar errores y restaurar estado original
                provincia.nombre = nombre_original
                db.session.rollback()
                flash('Error al actualizar la provincia', 'error')
                print(f"Error actualizando provincia: {e}")
        
        return render_template('admin/editar_provincia.html', provincia=provincia)
    
    @staticmethod
    @login_required
    def eliminar_provincia(provincia_id):
        """
        Elimina una provincia del sistema.
        
        Verifica que no tenga ciudades asociadas antes de eliminar
        para mantener la integridad referencial.
        
        Args:
            provincia_id (int): ID de la provincia a eliminar
            
        Returns:
            redirect: Redirección a la lista con mensaje de resultado
        """
        provincia = Provincia.query.get_or_404(provincia_id)
        
        # Verificar integridad referencial - no eliminar si tiene ciudades
        if provincia.ciudades:
            flash('No se puede eliminar la provincia porque tiene ciudades asociadas', 'error')
            return redirect(url_for('admin.listar_provincias'))
        
        # Intentar eliminar la provincia
        try:
            db.session.delete(provincia)
            db.session.commit()
            flash('Provincia eliminada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al eliminar la provincia', 'error')
            print(f"Error eliminando provincia: {e}")
        
        return redirect(url_for('admin.listar_provincias'))
    
    # ===== GESTIÓN DE CIUDADES =====
    
    @staticmethod
    @login_required
    def listar_ciudades():
        """
        Lista todas las ciudades del sistema con sus provincias.
        
        Obtiene todas las ciudades ordenadas alfabéticamente junto con
        las provincias disponibles para el formulario de creación.
        
        Returns:
            render_template: Página con lista de ciudades y formularios
        """
        # Obtener ciudades con sus provincias mediante JOIN
        ciudades = Ciudad.query.join(Provincia).order_by(Ciudad.nombre).all()
        
        # Obtener provincias para el selector del formulario
        provincias = Provincia.obtener_todas()
        
        # Obtener todas las ciudades para el formulario de conexiones
        todas_ciudades = Ciudad.obtener_todas()
        
        return render_template('admin/ciudades.html', 
                            ciudades=ciudades, 
                            provincias=provincias,
                            todas_ciudades=todas_ciudades)
    
    @staticmethod
    @login_required
    def crear_ciudad():
        """
        Crea una nueva ciudad con sus conexiones de rutas.
        
        Proceso:
        1. Valida datos básicos de la ciudad
        2. Crea la ciudad en la base de datos
        3. Crea las rutas de conexión especificadas
        4. Maneja errores y rollback si es necesario
        
        Returns:
            redirect: Redirección a la lista con mensaje de resultado
        """
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form.get('nombre', '').strip()
            es_costera = request.form.get('es_costera') == 'on'  # Checkbox
            provincia_id = request.form.get('provincia_id')
            ciudades_conectadas = request.form.getlist('ciudades_conectadas')
            costos = request.form.getlist('costos')
            
            # Validación básica de datos obligatorios
            if not nombre:
                flash('El nombre de la ciudad es obligatorio', 'error')
                return redirect(url_for('admin.listar_ciudades'))
            
            # Validar que se especifique una provincia
            if not provincia_id:
                flash('La provincia es obligatoria', 'error')
                return redirect(url_for('admin.listar_ciudades'))
            
            # Crear objeto temporal para ejecutar validaciones
            nueva_ciudad = Ciudad(
                nombre=nombre,
                es_costera=es_costera,
                provincia_id=int(provincia_id)
            )
            
            # Validar nombre de la ciudad
            es_valido, mensaje = nueva_ciudad.validate_nombre()
            if not es_valido:
                flash(mensaje, 'error')
                return redirect(url_for('admin.listar_ciudades'))
            
            # Validar que la provincia exista
            es_valido, mensaje = nueva_ciudad.validate_provincia()
            if not es_valido:
                flash(mensaje, 'error')
                return redirect(url_for('admin.listar_ciudades'))
            
            # Intentar crear la ciudad y sus rutas
            try:
                # Agregar ciudad a la sesión y obtener ID
                db.session.add(nueva_ciudad)
                db.session.flush()  # Para obtener el ID de la nueva ciudad
                
                # Crear rutas no dirigidas (una sola entrada por conexión)
                for i, ciudad_destino_id in enumerate(ciudades_conectadas):
                    if ciudad_destino_id and i < len(costos) and costos[i]:
                        costo = float(costos[i])
                        
                        # Verificar que no exista ya una conexión entre estas ciudades
                        if not Ruta.existe_conexion(nueva_ciudad.id, int(ciudad_destino_id)):
                            # Crear ruta (bidireccional por ser grafo no dirigido)
                            ruta = Ruta(
                                ciudad_origen_id=nueva_ciudad.id,
                                ciudad_destino_id=int(ciudad_destino_id),
                                costo=costo
                            )
                            db.session.add(ruta)
                
                db.session.commit()
                flash('Ciudad creada exitosamente con rutas no dirigidas', 'success')
                
            except ValueError:
                # Error en conversión de datos numéricos
                db.session.rollback()
                flash('Error en los datos ingresados. Verifique los costos.', 'error')
            except Exception as e:
                # Error general de base de datos
                db.session.rollback()
                flash('Error al crear la ciudad', 'error')
                print(f"Error creando ciudad: {e}")
        
        return redirect(url_for('admin.listar_ciudades'))
    
    @staticmethod
    @login_required
    def editar_ciudad(ciudad_id):
        """
        Edita una ciudad existente y permite modificar sus conexiones.
        
        Args:
            ciudad_id (int): ID de la ciudad a editar
            
        Returns:
            render_template/redirect: Página de edición o redirección con mensaje
        """
        # Obtener ciudad y datos relacionados
        ciudad = Ciudad.query.get_or_404(ciudad_id)
        provincias = Provincia.obtener_todas()
        todas_ciudades = Ciudad.query.filter(Ciudad.id != ciudad_id).all()
        
        # Obtener rutas existentes conectadas a esta ciudad (en ambas direcciones)
        rutas_existentes = Ruta.obtener_por_ciudad(ciudad_id)
        
        if request.method == 'POST':
            # Obtener datos del formulario
            nombre = request.form.get('nombre', '').strip()
            es_costera = request.form.get('es_costera') == 'on'
            provincia_id = request.form.get('provincia_id')
            
            # Validación básica
            if not nombre:
                flash('El nombre de la ciudad es obligatorio', 'error')
                return render_template('admin/editar_ciudad.html', 
                                    ciudad=ciudad, provincias=provincias, 
                                    todas_ciudades=todas_ciudades, rutas_existentes=rutas_existentes)
            
            if not provincia_id:
                flash('La provincia es obligatoria', 'error')
                return render_template('admin/editar_ciudad.html', 
                                    ciudad=ciudad, provincias=provincias,
                                    todas_ciudades=todas_ciudades, rutas_existentes=rutas_existentes)
            
            # Guardar valores originales
            nombre_original = ciudad.nombre
            es_costera_original = ciudad.es_costera
            provincia_id_original = ciudad.provincia_id
            
            # Actualizar valores temporalmente para validar
            ciudad.nombre = nombre
            ciudad.es_costera = es_costera
            ciudad.provincia_id = int(provincia_id)
            
            # Validar nombre
            es_valido, mensaje = ciudad.validate_nombre()
            if not es_valido:
                # Restaurar valores originales
                ciudad.nombre = nombre_original
                ciudad.es_costera = es_costera_original
                ciudad.provincia_id = provincia_id_original
                flash(mensaje, 'error')
                return render_template('admin/editar_ciudad.html', 
                                    ciudad=ciudad, provincias=provincias,
                                    todas_ciudades=todas_ciudades, rutas_existentes=rutas_existentes)
            
            # Validar provincia
            es_valido, mensaje = ciudad.validate_provincia()
            if not es_valido:
                # Restaurar valores originales
                ciudad.nombre = nombre_original
                ciudad.es_costera = es_costera_original
                ciudad.provincia_id = provincia_id_original
                flash(mensaje, 'error')
                return render_template('admin/editar_ciudad.html', 
                                    ciudad=ciudad, provincias=provincias,
                                    todas_ciudades=todas_ciudades, rutas_existentes=rutas_existentes)
            
            try:
                db.session.commit()
                flash('Ciudad actualizada exitosamente', 'success')
                return redirect(url_for('admin.listar_ciudades'))
            except Exception as e:
                # Restaurar valores originales
                ciudad.nombre = nombre_original
                ciudad.es_costera = es_costera_original
                ciudad.provincia_id = provincia_id_original
                db.session.rollback()
                flash('Error al actualizar la ciudad', 'error')
        
        return render_template('admin/editar_ciudad.html', 
                            ciudad=ciudad, provincias=provincias,
                            todas_ciudades=todas_ciudades, rutas_existentes=rutas_existentes)
    
    @staticmethod
    @login_required
    def eliminar_ciudad(ciudad_id):
        """Elimina una ciudad y todas sus rutas"""
        ciudad = Ciudad.query.get_or_404(ciudad_id)
        
        try:
            # Eliminar todas las rutas asociadas (tanto de origen como de destino)
            Ruta.query.filter(
                (Ruta.ciudad_origen_id == ciudad_id) | 
                (Ruta.ciudad_destino_id == ciudad_id)
            ).delete()
            
            # Eliminar la ciudad
            db.session.delete(ciudad)
            db.session.commit()
            flash('Ciudad y sus rutas eliminadas exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al eliminar la ciudad', 'error')
        
        return redirect(url_for('admin.listar_ciudades'))
    
    @staticmethod
    @login_required
    def listar_rutas():
        """Lista todas las rutas"""
        from sqlalchemy.orm import aliased
        
        # Crear alias para las ciudades de origen y destino
        CiudadOrigen = aliased(Ciudad)
        CiudadDestino = aliased(Ciudad)
        
        rutas = Ruta.query.join(
            CiudadOrigen, Ruta.ciudad_origen_id == CiudadOrigen.id
        ).join(
            CiudadDestino, Ruta.ciudad_destino_id == CiudadDestino.id
        ).all()
        
        # Obtener todas las ciudades para el modal de añadir ruta
        ciudades = Ciudad.query.all()
        
        return render_template('admin/rutas.html', rutas=rutas, ciudades=ciudades)
    
    @staticmethod
    @login_required
    def obtener_ciudades_por_provincia():
        """API endpoint para obtener ciudades de una provincia"""
        provincia_id = request.args.get('provincia_id')
        if provincia_id:
            ciudades = Ciudad.query.filter_by(provincia_id=provincia_id).all()
            return jsonify([ciudad.to_dict() for ciudad in ciudades])
        return jsonify([])
    
    @staticmethod
    @login_required
    def agregar_ruta_ciudad():
        """Agrega una conexión no dirigida a una ciudad existente"""
        ciudad_id = request.form.get('ciudad_id')
        ciudad_destino_id = request.form.get('ciudad_destino_id')
        costo = request.form.get('costo')
        
        if not all([ciudad_id, ciudad_destino_id, costo]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('admin.editar_ciudad', ciudad_id=ciudad_id))
        
        try:
            costo = float(costo)
            ciudad_id = int(ciudad_id)
            ciudad_destino_id = int(ciudad_destino_id)
            
            # Verificar que no exista ya la conexión (en cualquier dirección)
            if Ruta.existe_conexion(ciudad_id, ciudad_destino_id):
                flash('Ya existe una conexión entre estas ciudades', 'error')
                return redirect(url_for('admin.editar_ciudad', ciudad_id=ciudad_id))
            
            # Crear una sola ruta (el grafo no dirigido la interpretará en ambas direcciones)
            ruta = Ruta(
                ciudad_origen_id=ciudad_id,
                ciudad_destino_id=ciudad_destino_id,
                costo=costo
            )
            
            db.session.add(ruta)
            db.session.commit()
            flash('Conexión no dirigida agregada exitosamente', 'success')
            
        except ValueError:
            flash('Error en los datos ingresados', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar la conexión', 'error')
        
        return redirect(url_for('admin.editar_ciudad', ciudad_id=ciudad_id))
    
    @staticmethod
    @login_required
    def eliminar_ruta():
        """Elimina una conexión no dirigida"""
        ruta_id = request.form.get('ruta_id')
        ciudad_id = request.form.get('ciudad_id')
        
        try:
            ruta = Ruta.query.get_or_404(ruta_id)
            
            # En un grafo no dirigido, solo necesitamos eliminar una entrada
            # pero debemos buscar si existe la ruta inversa (por datos anteriores)
            ruta_inversa = Ruta.query.filter(
                (Ruta.ciudad_origen_id == ruta.ciudad_destino_id) &
                (Ruta.ciudad_destino_id == ruta.ciudad_origen_id) &
                (Ruta.id != ruta.id)
            ).first()
            
            db.session.delete(ruta)
            if ruta_inversa:
                db.session.delete(ruta_inversa)
            
            db.session.commit()
            flash('Conexión eliminada exitosamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Error al eliminar la conexión', 'error')
        
        return redirect(url_for('admin.editar_ciudad', ciudad_id=ciudad_id))
    
    @staticmethod
    @login_required
    def crear_ruta_directa():
        """Crea una nueva ruta directamente desde la sección de rutas"""
        if request.method == 'POST':
            ciudad_origen_id = request.form.get('ciudad_origen_id')
            ciudad_destino_id = request.form.get('ciudad_destino_id')
            costo = request.form.get('costo')
            
            if not all([ciudad_origen_id, ciudad_destino_id, costo]):
                flash('Todos los campos son obligatorios', 'error')
                return redirect(url_for('admin.listar_rutas'))
            
            try:
                costo = float(costo)
                ciudad_origen_id = int(ciudad_origen_id)
                ciudad_destino_id = int(ciudad_destino_id)
                
                # Validar que las ciudades sean diferentes
                if ciudad_origen_id == ciudad_destino_id:
                    flash('La ciudad de origen y destino deben ser diferentes', 'error')
                    return redirect(url_for('admin.listar_rutas'))
                
                # Obtener nombres de ciudades para mensaje más descriptivo
                ciudad_origen = Ciudad.query.get(ciudad_origen_id)
                ciudad_destino = Ciudad.query.get(ciudad_destino_id)
                
                if not ciudad_origen or not ciudad_destino:
                    flash('Una o ambas ciudades seleccionadas no existen', 'error')
                    return redirect(url_for('admin.listar_rutas'))
                
                # Verificar que no exista ya la conexión (en cualquier dirección)
                if Ruta.existe_conexion(ciudad_origen_id, ciudad_destino_id):
                    flash(f'Ya existe una conexión entre {ciudad_origen.nombre} y {ciudad_destino.nombre}', 'error')
                    return redirect(url_for('admin.listar_rutas'))
                
                # Crear una sola ruta (el grafo no dirigido la interpretará en ambas direcciones)
                ruta = Ruta(
                    ciudad_origen_id=ciudad_origen_id,
                    ciudad_destino_id=ciudad_destino_id,
                    costo=costo
                )
                
                db.session.add(ruta)
                db.session.commit()
                flash(f'Conexión entre {ciudad_origen.nombre} y {ciudad_destino.nombre} creada exitosamente (costo: ${costo:.2f})', 'success')
                
            except ValueError:
                flash('Error en los datos ingresados. Verifique que el costo sea un número válido', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear la conexión: {str(e)}', 'error')
        
        return redirect(url_for('admin.listar_rutas'))
    
    @staticmethod
    @login_required
    def editar_ruta_directa():
        """Edita el costo de una ruta existente desde la sección de rutas"""
        if request.method == 'POST':
            ruta_id = request.form.get('ruta_id')
            nuevo_costo = request.form.get('costo')
            
            if not all([ruta_id, nuevo_costo]):
                flash('Todos los campos son obligatorios', 'error')
                return redirect(url_for('admin.listar_rutas'))
            
            try:
                nuevo_costo = float(nuevo_costo)
                ruta_id = int(ruta_id)
                
                # Validar que el costo sea positivo
                if nuevo_costo <= 0:
                    flash('El costo debe ser mayor a 0', 'error')
                    return redirect(url_for('admin.listar_rutas'))
                
                # Buscar la ruta
                ruta = Ruta.query.get(ruta_id)
                if not ruta:
                    flash('La ruta especificada no existe', 'error')
                    return redirect(url_for('admin.listar_rutas'))
                
                # Obtener nombres de ciudades para mensaje más descriptivo
                ciudad_origen = ruta.ciudad_origen
                ciudad_destino = ruta.ciudad_destino
                costo_anterior = ruta.costo
                
                # Actualizar el costo
                ruta.costo = nuevo_costo
                
                # Buscar si existe una ruta inversa (para mantener consistencia en grafos no dirigidos)
                ruta_inversa = Ruta.query.filter(
                    (Ruta.ciudad_origen_id == ruta.ciudad_destino_id) &
                    (Ruta.ciudad_destino_id == ruta.ciudad_origen_id) &
                    (Ruta.id != ruta.id)
                ).first()
                
                if ruta_inversa:
                    ruta_inversa.costo = nuevo_costo
                
                db.session.commit()
                flash(f'Costo actualizado de ${costo_anterior:.2f} a ${nuevo_costo:.2f} para la conexión entre {ciudad_origen.nombre} y {ciudad_destino.nombre}', 'success')
                
            except ValueError:
                flash('Error en los datos ingresados. Verifique que el costo sea un número válido', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar el costo: {str(e)}', 'error')
        
        return redirect(url_for('admin.listar_rutas'))
    
    @staticmethod
    @login_required
    def eliminar_ruta_directa():
        """Elimina una ruta directamente desde la sección de rutas"""
        if request.method == 'POST':
            ruta_id = request.form.get('ruta_id')
            
            if not ruta_id:
                flash('ID de ruta es obligatorio', 'error')
                return redirect(url_for('admin.listar_rutas'))
            
            try:
                ruta_id = int(ruta_id)
                
                # Buscar la ruta
                ruta = Ruta.query.get(ruta_id)
                if not ruta:
                    flash('La ruta especificada no existe', 'error')
                    return redirect(url_for('admin.listar_rutas'))
                
                # Obtener nombres de ciudades para mensaje más descriptivo
                ciudad_origen = ruta.ciudad_origen
                ciudad_destino = ruta.ciudad_destino
                costo = ruta.costo
                
                # Buscar si existe una ruta inversa (para eliminarla también en grafos no dirigidos)
                ruta_inversa = Ruta.query.filter(
                    (Ruta.ciudad_origen_id == ruta.ciudad_destino_id) &
                    (Ruta.ciudad_destino_id == ruta.ciudad_origen_id) &
                    (Ruta.id != ruta.id)
                ).first()
                
                # Eliminar la ruta principal
                db.session.delete(ruta)
                
                # Eliminar la ruta inversa si existe
                if ruta_inversa:
                    db.session.delete(ruta_inversa)
                
                db.session.commit()
                flash(f'Conexión entre {ciudad_origen.nombre} y {ciudad_destino.nombre} (costo: ${costo:.2f}) eliminada exitosamente', 'success')
                
            except ValueError:
                flash('Error en el ID de la ruta', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al eliminar la conexión: {str(e)}', 'error')
        
        return redirect(url_for('admin.listar_rutas'))
