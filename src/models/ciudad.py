"""
Modelo de Ciudad
===============

Este módulo define el modelo de datos para las ciudades del sistema.
Las ciudades representan los nodos del grafo en el algoritmo de rutas.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from extensions import db

class Ciudad(db.Model):
    """
    Modelo que representa una ciudad en el sistema de rutas.
    
    Las ciudades actúan como nodos en el grafo utilizado por el algoritmo de Dijkstra.
    Cada ciudad pertenece a una provincia y puede ser costera o no.
    """
    
    __tablename__ = 'ciudades'
    
    # Campos de la tabla ciudades
    id = db.Column(db.Integer, primary_key=True)                                    # ID único de la ciudad
    nombre = db.Column(db.String(100), nullable=False)                             # Nombre de la ciudad
    es_costera = db.Column(db.Boolean, nullable=False)                             # Indica si es ciudad costera
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincias.id'), nullable=False)  # ID de la provincia
    
    # Relaciones con otras tablas
    # Una ciudad puede ser origen de múltiples rutas
    rutas_origen = db.relationship('Ruta', foreign_keys='Ruta.ciudad_origen_id', 
                                  backref='ciudad_origen', lazy=True)
    # Una ciudad puede ser destino de múltiples rutas
    rutas_destino = db.relationship('Ruta', foreign_keys='Ruta.ciudad_destino_id', 
                                   backref='ciudad_destino', lazy=True)

    def __repr__(self):
        """Representación string del objeto Ciudad para debugging."""
        return f'<Ciudad {self.nombre}>'
    
    def to_dict(self):
        """
        Convierte el objeto Ciudad a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los datos de la ciudad
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'es_costera': self.es_costera,
            'provincia_id': self.provincia_id,
            'provincia_nombre': self.provincia.nombre if self.provincia else None
        }
    
    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las ciudades ordenadas alfabéticamente por nombre.
        
        Returns:
            list: Lista de objetos Ciudad ordenados por nombre
        """
        return Ciudad.query.order_by(Ciudad.nombre).all()
    
    @staticmethod
    def obtener_costeras():
        """
        Obtiene solo las ciudades costeras ordenadas por nombre.
        
        Returns:
            list: Lista de ciudades costeras
        """
        return Ciudad.query.filter_by(es_costera=True).order_by(Ciudad.nombre).all()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        """
        Busca una ciudad por su nombre exacto.
        
        Args:
            nombre (str): Nombre de la ciudad a buscar
            
        Returns:
            Ciudad: Objeto Ciudad encontrado o None si no existe
        """
        return cls.query.filter_by(nombre=nombre).first()
    
    def validate_nombre(self):
        """
        Valida que el nombre de la ciudad cumpla con los requisitos.
        
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        import re
        
        # Verificar que no esté vacío
        if not self.nombre or not self.nombre.strip():
            return False, "El nombre de la ciudad no puede estar vacío"
        
        # Verificar que solo contenga letras, espacios y acentos
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', self.nombre.strip()):
            return False, "El nombre de la ciudad solo puede contener letras y espacios"
        
        # Verificar que no tenga espacios múltiples o al inicio/final
        if '  ' in self.nombre or self.nombre.strip() != self.nombre:
            return False, "El nombre no puede tener espacios múltiples o al inicio/final"
        
        # Verificar unicidad del nombre (case insensitive)
        existente = Ciudad.query.filter(
            db.func.lower(Ciudad.nombre) == self.nombre.lower(),
            Ciudad.id != self.id  # Excluir la ciudad actual en caso de actualización
        ).first()
        
        if existente:
            return False, "El nombre de la ciudad ya existe"
        
        return True, "Válido"
    
    def validate_es_costera(self):
        """
        Valida que el campo es_costera sea un valor booleano válido.
        
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        if self.es_costera not in [True, False]:
            return False, "El campo 'es costera' debe ser True o False"
        return True, "Válido"
    
    def validate_provincia(self):
        """
        Valida que la provincia asociada exista en la base de datos.
        
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        from models.provincia import Provincia
        
        # Verificar que se haya proporcionado una provincia
        if not self.provincia_id:
            return False, "La provincia es obligatoria"
        
        # Verificar que la provincia exista
        provincia = Provincia.query.get(self.provincia_id)
        if not provincia:
            return False, "La provincia seleccionada no existe"
        
        return True, "Válido"
