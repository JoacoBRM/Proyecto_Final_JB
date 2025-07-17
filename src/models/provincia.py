"""
Modelo de Provincia
==================

Este módulo define el modelo de datos para las provincias del sistema.
Las provincias agrupan ciudades para organización territorial.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from extensions import db

class Provincia(db.Model):
    """
    Modelo que representa una provincia en el sistema.
    
    Las provincias agrupan ciudades para facilitar la organización
    territorial y administrativa del sistema de rutas.
    """
    
    __tablename__ = 'provincias'
    
    # Campos de la tabla provincias
    id = db.Column(db.Integer, primary_key=True)                        # ID único de la provincia
    nombre = db.Column(db.String(100), nullable=False, unique=True)     # Nombre único de la provincia
    
    # Relación con ciudades (una provincia tiene muchas ciudades)
    ciudades = db.relationship('Ciudad', backref='provincia', lazy=True)
    
    def __repr__(self):
        """Representación string del objeto Provincia para debugging."""
        return f'<Provincia {self.nombre}>'
    
    def to_dict(self):
        """
        Convierte el objeto Provincia a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los datos de la provincia
        """
        return {
            'id': self.id,
            'nombre': self.nombre
        }
    
    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las provincias ordenadas alfabéticamente por nombre.
        
        Returns:
            list: Lista de objetos Provincia ordenados por nombre
        """
        return Provincia.query.order_by(Provincia.nombre).all()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        """
        Busca una provincia por su nombre exacto.
        
        Args:
            nombre (str): Nombre de la provincia a buscar
            
        Returns:
            Provincia: Objeto Provincia encontrado o None si no existe
        """
        return cls.query.filter_by(nombre=nombre).first()
    
    def validate_name(self):
        """
        Valida que el nombre de la provincia cumpla con los requisitos.
        
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        import re
        
        # Verificar que no esté vacío
        if not self.nombre or not self.nombre.strip():
            return False, "El nombre de la provincia no puede estar vacío"
        
        # Verificar que solo contenga letras, espacios y acentos
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', self.nombre.strip()):
            return False, "El nombre de la provincia solo puede contener letras y espacios"
        
        # Verificar que no tenga espacios múltiples o al inicio/final
        if '  ' in self.nombre or self.nombre.strip() != self.nombre:
            return False, "El nombre no puede tener espacios múltiples o al inicio/final"
        
        # Verificar unicidad del nombre (case insensitive)
        existente = Provincia.query.filter(
            db.func.lower(Provincia.nombre) == self.nombre.lower(),
            Provincia.id != self.id  # Excluir la provincia actual en caso de actualización
        ).first()
        
        if existente:
            return False, "El nombre de la provincia ya existe"
        
        return True, "Válido"