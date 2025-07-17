"""
Modelo de Ruta
=============

Este módulo define el modelo de datos para las rutas del sistema.
Las rutas representan las aristas del grafo con sus costos asociados.

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from extensions import db
from decimal import Decimal

class Ruta(db.Model):
    """
    Modelo que representa una ruta entre dos ciudades.
    
    Las rutas actúan como aristas ponderadas en el grafo utilizado por
    el algoritmo de Dijkstra. Cada ruta conecta dos ciudades con un costo específico.
    El grafo es no dirigido, por lo que una ruta permite el tránsito en ambas direcciones.
    """
    
    __tablename__ = 'rutas'
    
    # Campos de la tabla rutas
    id = db.Column(db.Integer, primary_key=True)                                          # ID único de la ruta
    ciudad_origen_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)   # ID ciudad origen
    ciudad_destino_id = db.Column(db.Integer, db.ForeignKey('ciudades.id'), nullable=False)  # ID ciudad destino
    costo = db.Column(db.Numeric(10, 2), nullable=False)                                 # Costo de la ruta (distancia, tiempo, etc.)

    def __repr__(self):
        """Representación string del objeto Ruta para debugging."""
        return f'<Conexión {self.id}: {self.ciudad_origen.nombre} ↔ {self.ciudad_destino.nombre} (costo: {self.costo})>'
    
    def to_dict(self):
        """
        Convierte el objeto Ruta a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los datos de la ruta
        """
        return {
            'id': self.id,
            'ciudad_origen_id': self.ciudad_origen_id,
            'ciudad_destino_id': self.ciudad_destino_id,
            'ciudad_origen_nombre': self.ciudad_origen.nombre if self.ciudad_origen else None,
            'ciudad_destino_nombre': self.ciudad_destino.nombre if self.ciudad_destino else None,
            'costo': float(self.costo)
        }
    
    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las rutas del sistema.
        
        Returns:
            list: Lista de objetos Ruta
        """
        return Ruta.query.all()
    
    @staticmethod
    def obtener_por_origen(ciudad_id):
        """
        Obtiene todas las rutas que parten de una ciudad específica.
        
        Args:
            ciudad_id (int): ID de la ciudad origen
            
        Returns:
            list: Lista de rutas que tienen como origen la ciudad especificada
        """
        return Ruta.query.filter_by(ciudad_origen_id=ciudad_id).all()
    
    @staticmethod
    def obtener_por_destino(ciudad_id):
        """
        Obtiene todas las rutas que llegan a una ciudad específica.
        
        Args:
            ciudad_id (int): ID de la ciudad destino
            
        Returns:
            list: Lista de rutas que tienen como destino la ciudad especificada
        """
        return Ruta.query.filter_by(ciudad_destino_id=ciudad_id).all()
    
    @staticmethod
    def obtener_por_ciudad(ciudad_id):
        """
        Obtiene todas las rutas conectadas a una ciudad (tanto como origen como destino).
        Útil para construir el grafo y encontrar todas las conexiones de un nodo.
        
        Args:
            ciudad_id (int): ID de la ciudad
            
        Returns:
            list: Lista de rutas conectadas a la ciudad especificada
        """
        return Ruta.query.filter(
            (Ruta.ciudad_origen_id == ciudad_id) | (Ruta.ciudad_destino_id == ciudad_id)
        ).all()
    
    @classmethod
    def buscar_ruta_directa(cls, origen_id, destino_id):
        """
        Busca una ruta directa entre dos ciudades en cualquier dirección.
        Como el grafo es no dirigido, busca en ambas direcciones.
        
        Args:
            origen_id (int): ID de la primera ciudad
            destino_id (int): ID de la segunda ciudad
            
        Returns:
            Ruta: Objeto Ruta encontrado o None si no existe conexión directa
        """
        return cls.query.filter(
            ((cls.ciudad_origen_id == origen_id) & (cls.ciudad_destino_id == destino_id)) |
            ((cls.ciudad_origen_id == destino_id) & (cls.ciudad_destino_id == origen_id))
        ).first()

    @classmethod
    def existe_conexion(cls, ciudad1_id, ciudad2_id):
        """
        Verifica si existe una conexión directa entre dos ciudades.
        
        Args:
            ciudad1_id (int): ID de la primera ciudad
            ciudad2_id (int): ID de la segunda ciudad
            
        Returns:
            bool: True si existe conexión, False en caso contrario
        """
        # Buscar en ambas direcciones para grafo no dirigido
        ruta_directa = cls.query.filter(
            ((cls.ciudad_origen_id == ciudad1_id) & (cls.ciudad_destino_id == ciudad2_id))
        ).first()
        
        ruta_inversa = cls.query.filter(
            ((cls.ciudad_origen_id == ciudad2_id) & (cls.ciudad_destino_id == ciudad1_id))
        ).first()
        
        return ruta_directa is not None or ruta_inversa is not None

    def get_ciudad_conectada(self, ciudad_id):
        """
        Obtiene la ciudad conectada a la ciudad especificada en esta ruta.
        
        Args:
            ciudad_id (int): ID de una de las ciudades de la ruta
            
        Returns:
            Ciudad: Objeto Ciudad conectado o None si la ciudad no está en esta ruta
        """
        if self.ciudad_origen_id == ciudad_id:
            return self.ciudad_destino
        elif self.ciudad_destino_id == ciudad_id:
            return self.ciudad_origen
        return None

    def contiene_ciudad(self, ciudad_id):
        """
        Verifica si la ruta conecta con la ciudad especificada.
        
        Args:
            ciudad_id (int): ID de la ciudad a verificar
            
        Returns:
            bool: True si la ciudad está en esta ruta, False en caso contrario
        """
        return self.ciudad_origen_id == ciudad_id or self.ciudad_destino_id == ciudad_id

    def validate_ciudades(self):
        """
        Valida que las ciudades de origen y destino sean válidas y no duplicadas.
        
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        # Verificar que ambas ciudades estén especificadas
        if not self.ciudad_origen_id or not self.ciudad_destino_id:
            return False, "Las ciudades de origen y destino son obligatorias"
        
        # Verificar que no sean la misma ciudad
        if self.ciudad_origen_id == self.ciudad_destino_id:
            return False, "Las ciudades de origen y destino no pueden ser la misma"
        
        # Validar que no exista una ruta duplicada en ambas direcciones (grafo no dirigido)
        existente = Ruta.query.filter(
            (
                ((Ruta.ciudad_origen_id == self.ciudad_origen_id) & (Ruta.ciudad_destino_id == self.ciudad_destino_id)) |
                ((Ruta.ciudad_origen_id == self.ciudad_destino_id) & (Ruta.ciudad_destino_id == self.ciudad_origen_id))
            ) &
            (Ruta.id != self.id)  # Excluir la ruta actual en caso de actualización
        ).first()
        
        if existente:
            return False, "Ya existe una conexión entre estas dos ciudades"
        
        return True, "Válido"
    
    def validate_costo(self):
        """
        Valida que el costo de la ruta sea un valor positivo válido.
        
        Returns:
            tuple: (es_valido: bool, mensaje: str)
        """
        if self.costo is None or self.costo <= 0:
            return False, "El costo debe ser un número positivo"
        return True, "Válido"