"""
Utilidades para Grafos con Base de Datos
=======================================

Este módulo contiene todas las funciones de utilidad para trabajar con grafos
usando datos dinámicos de la base de datos. Implementa el algoritmo de Dijkstra
utilizando NetworkX y maneja visualizaciones del grafo.

IMPORTANTE: Este sistema maneja grafos NO DIRIGIDOS (undirected graphs).
- Una sola entrada en la base de datos representa una conexión bidireccional
- No se crean rutas duplicadas en ambas direcciones
- El grafo de NetworkX es de tipo Graph (no DiGraph)

Funcionalidades principales:
- Construcción de grafos desde base de datos
- Algoritmo de Dijkstra para rutas óptimas
- Visualización de grafos y caminos
- Estadísticas del sistema de rutas
- Validaciones de ciudades

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

import matplotlib
matplotlib.use('Agg')  # Backend sin interfaz gráfica para uso en servidor
import matplotlib.pyplot as plt
import networkx as nx
import io
from models import Ciudad
from models import Ruta


def construir_grafo():
    """
    Construye un grafo no dirigido y ponderado desde la base de datos.
    
    El grafo se crea dinámicamente obteniendo todas las rutas almacenadas
    en la base de datos. Cada ruta representa una arista bidireccional.
    
    Returns:
        nx.Graph: Grafo no dirigido con ciudades como nodos y rutas como aristas ponderadas
    """
    G = nx.Graph()  # Grafo no dirigido (bidireccional)
    
    # Obtener todas las rutas de la base de datos
    rutas = Ruta.query.all()
    
    # Agregar cada ruta como arista ponderada
    for ruta in rutas:
        origen = ruta.ciudad_origen.nombre
        destino = ruta.ciudad_destino.nombre
        costo = float(ruta.costo)
        
        # En un grafo no dirigido, una arista conecta en ambas direcciones automáticamente
        G.add_edge(origen, destino, weight=costo)
    
    return G


def obtener_ciudades_costeras():
    """
    Obtiene el conjunto de ciudades costeras desde la base de datos.
    
    Returns:
        set: Conjunto con los nombres de las ciudades costeras
    """
    ciudades_costeras = Ciudad.obtener_costeras()
    return {ciudad.nombre for ciudad in ciudades_costeras}


def obtener_ciudades():
    """
    Obtiene la lista de todas las ciudades desde la base de datos.
    
    Returns:
        list: Lista con los nombres de todas las ciudades ordenadas alfabéticamente
    """
    ciudades = Ciudad.obtener_todas()
    return [ciudad.nombre for ciudad in ciudades]


def grafo_a_imagen():
    """
    Genera una imagen visual del grafo completo del sistema.
    
    Crea una representación gráfica usando NetworkX y Matplotlib,
    mostrando todas las ciudades y sus conexiones.
    
    Returns:
        io.BytesIO: Buffer con la imagen PNG del grafo
    """
    # Construir el grafo desde la base de datos
    G = construir_grafo()
    
    # Calcular posiciones de los nodos usando algoritmo spring layout
    pos = nx.spring_layout(G, seed=8)  # seed para posiciones consistentes
    
    # Obtener los pesos de las aristas para mostrar en las etiquetas
    pesos = nx.get_edge_attributes(G, 'weight')

    # Crear la figura y dibujar el grafo
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Dibujar nodos y aristas (sin flechas porque es grafo no dirigido)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, 
            font_weight='bold')
    
    # Dibujar etiquetas con los costos de las aristas
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)
    
    # Guardar la imagen en un buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()  # Liberar memoria
    
    return buf


def camino_optimo_con_costera(origen='Ibarra', destino='Loja'):
    """
    Calcula el camino óptimo entre dos ciudades usando el algoritmo de Dijkstra.
    
    Esta función implementa la lógica principal del sistema: encontrar la ruta
    más corta entre dos puntos y verificar si pasa por ciudades costeras.
    
    Args:
        origen (str): Nombre de la ciudad origen
        destino (str): Nombre de la ciudad destino
        
    Returns:
        dict: Diccionario con el camino, costo, validez y ciudades costeras
              - camino: Lista de ciudades en la ruta óptima
              - costo: Costo total de la ruta
              - valido: True si pasa por al menos una ciudad costera
              - ciudades_costeras_en_ruta: Lista de ciudades costeras en la ruta
    """
    # Construir el grafo desde la base de datos
    G = construir_grafo()
    
    # Obtener conjunto de ciudades costeras
    costeras = obtener_ciudades_costeras()

    try:
        # Aplicar algoritmo de Dijkstra para encontrar el camino más corto
        camino = nx.dijkstra_path(G, origen, destino, weight='weight')
        costo = nx.dijkstra_path_length(G, origen, destino, weight='weight')

        # Verificar si el camino pasa por al menos una ciudad costera
        contiene_costera = any(ciudad in costeras for ciudad in camino)
        
        # Retornar resultado estructurado
        return {
            "camino": camino,
            "costo": costo,
            "valido": contiene_costera,
            "ciudades_costeras_en_ruta": [c for c in camino if c in costeras]
        }
    except nx.NetworkXNoPath:
        # Manejar caso donde no existe camino entre origen y destino
        return {
            "camino": [],
            "costo": None,
            "valido": False,
            "ciudades_costeras_en_ruta": []
        }


def grafo_a_imagen_camino(camino):
    """
    Genera una imagen del grafo con un camino específico resaltado.
    
    Útil para visualizar la ruta óptima encontrada por el algoritmo de Dijkstra,
    destacándola en color diferente sobre el grafo completo.
    
    Args:
        camino (list): Lista de nombres de ciudades que forman la ruta
        
    Returns:
        io.BytesIO: Buffer con la imagen PNG del grafo con camino resaltado
    """
    # Construir el grafo desde la base de datos
    G = construir_grafo()
    
    # Calcular posiciones consistentes de los nodos
    pos = nx.spring_layout(G, seed=8)
    
    # Obtener pesos de las aristas para etiquetas
    pesos = nx.get_edge_attributes(G, 'weight')

    # Crear figura con fondo blanco
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')

    # Dibujar todos los nodos y aristas en colores base
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, 
            font_weight='bold', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, ax=ax)

    # Si hay camino proporcionado, resaltarlo en el grafo
    if camino and len(camino) > 1:
        # Crear lista de aristas que forman el camino
        edges_camino = list(zip(camino[:-1], camino[1:]))
        
        # Dibujar las aristas del camino en color rojo y más gruesas
        nx.draw_networkx_edges(G, pos, edgelist=edges_camino, edge_color='red', 
                            width=4, ax=ax)
        
        # Resaltar los nodos del camino en color naranja y más grandes
        nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='orange', 
                            node_size=2200, ax=ax)

    # Guardar la imagen en un buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close()  # Liberar memoria
    
    return buf


def obtener_estadisticas_grafo():
    """
    Obtiene estadísticas completas del grafo desde la base de datos.
    
    Calcula métricas importantes del sistema como número de ciudades,
    conexiones, rutas posibles y ejemplos de costos promedio.
    
    Returns:
        dict: Diccionario con todas las estadísticas del grafo
    """
    # Obtener datos básicos desde la base de datos
    ciudades = Ciudad.obtener_todas()
    ciudades_costeras = Ciudad.obtener_costeras()
    rutas = Ruta.obtener_todas()
    
    # En un grafo no dirigido, el número máximo de conexiones es n*(n-1)/2
    max_conexiones_posibles = len(ciudades) * (len(ciudades) - 1) // 2 if len(ciudades) > 1 else 0
    
    # Calcular algunas rutas de ejemplo para estadísticas de costo
    rutas_ejemplo = []
    ciudades_nombres = [c.nombre for c in ciudades]
    
    if len(ciudades_nombres) >= 3:
        # Usar las primeras ciudades disponibles para calcular rutas de ejemplo
        ejemplos = [
            (ciudades_nombres[0], ciudades_nombres[-1]),  # Primera a última
            (ciudades_nombres[1], ciudades_nombres[-2]) if len(ciudades_nombres) > 3 else (ciudades_nombres[0], ciudades_nombres[1]),
        ]
        
        # Calcular rutas de ejemplo usando Dijkstra
        for origen, destino in ejemplos:
            try:
                resultado = camino_optimo_con_costera(origen, destino)
                if resultado['costo'] is not None:
                    rutas_ejemplo.append(resultado)
            except:
                continue  # Ignorar errores en rutas de ejemplo
    
    # Calcular costo promedio de las rutas de ejemplo
    costo_promedio = 0
    if rutas_ejemplo:
        costo_promedio = sum(r['costo'] for r in rutas_ejemplo) / len(rutas_ejemplo)
    
    # Retornar estadísticas completas
    return {
        'total_ciudades': len(ciudades),
        'ciudades_costeras': len(ciudades_costeras),
        'total_conexiones': len(rutas),
        'conexiones_posibles': max_conexiones_posibles,
        'costo_promedio': round(costo_promedio, 2),
        'ciudades': ciudades_nombres,
        'tipo_grafo': 'No dirigido'
    }


def validar_ciudades_existen(origen, destino):
    """
    Valida que las ciudades de origen y destino existan en la base de datos.
    
    Args:
        origen (str): Nombre de la ciudad origen
        destino (str): Nombre de la ciudad destino
        
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    # Buscar ambas ciudades en la base de datos
    ciudad_origen = Ciudad.buscar_por_nombre(origen)
    ciudad_destino = Ciudad.buscar_por_nombre(destino)
    
    # Validar existencia de ciudad origen
    if not ciudad_origen:
        return False, f"La ciudad de origen '{origen}' no existe"
    
    # Validar existencia de ciudad destino
    if not ciudad_destino:
        return False, f"La ciudad de destino '{destino}' no existe"
    
    return True, "Ciudades válidas"


def obtener_rutas_desde_ciudad(ciudad_nombre):
    """
    Obtiene todas las rutas conectadas a una ciudad específica.
    
    Busca conexiones en ambas direcciones debido a que el grafo es no dirigido.
    
    Args:
        ciudad_nombre (str): Nombre de la ciudad
        
    Returns:
        list: Lista de tuplas (ciudad_conectada, costo)
    """
    # Buscar la ciudad en la base de datos
    ciudad = Ciudad.buscar_por_nombre(ciudad_nombre)
    if not ciudad:
        return []
    
    # Obtener todas las rutas que involucran esta ciudad
    rutas = Ruta.obtener_por_ciudad(ciudad.id)
    conexiones = []
    
    # Procesar cada ruta para obtener la ciudad conectada
    for ruta in rutas:
        ciudad_conectada = ruta.get_ciudad_conectada(ciudad.id)
        if ciudad_conectada:
            conexiones.append((ciudad_conectada.nombre, float(ruta.costo)))
    
    return conexiones


def obtener_todas_las_conexiones():
    """
    Obtiene todas las conexiones del grafo como lista de tuplas.
    
    Útil para análisis completo del grafo o exportación de datos.
    
    Returns:
        list: Lista de tuplas (origen, destino, costo) con todas las rutas
    """
    rutas = Ruta.obtener_todas()
    return [(ruta.ciudad_origen.nombre, ruta.ciudad_destino.nombre, float(ruta.costo)) for ruta in rutas]
