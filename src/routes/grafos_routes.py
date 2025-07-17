"""
Rutas de Grafos y Algoritmos
============================

Este módulo define las rutas relacionadas con la funcionalidad principal
del sistema: cálculo de rutas óptimas usando el algoritmo de Dijkstra.

Rutas incluidas:
- /grafos/: Página de introducción a los grafos
- /grafos/calcular_camino: Calculadora de rutas óptimas
- /grafos/camino: Ruta predefinida de ejemplo
- /grafos/grafo_imagen: Imagen del grafo completo
- /grafos/grafo_imagen_camino: Imagen con camino resaltado
- /grafos/exportar_pdf: Exportación de rutas a PDF

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import Blueprint
from flask_login import login_required
from controllers.grafo_controller import GrafoController

# Crear blueprint para rutas de grafos con prefijo URL
starter_bp = Blueprint('grafos', __name__, url_prefix='/grafos')

@starter_bp.route('/')
@login_required
def starter():
    """
    Página de introducción al sistema de grafos.
    
    Muestra estadísticas del sistema, información sobre el algoritmo
    de Dijkstra y acceso a las funcionalidades principales.
    
    Returns:
        Response: Página de introducción con estadísticas
    """
    return GrafoController.mostrar_introduccion()

@starter_bp.route('/calcular_camino', methods=['GET', 'POST'])
@login_required
def calcular_camino():
    """
    Calculadora de rutas óptimas entre ciudades.
    
    GET: Muestra formulario de selección de ciudades
    POST: Procesa el cálculo de ruta usando Dijkstra
    
    Returns:
        Response: Formulario o resultados del cálculo de ruta
    """
    return GrafoController.calcular_camino()

@starter_bp.route('/camino')
@login_required
def ver_camino():
    """
    Muestra una ruta predefinida de ejemplo (Ibarra - Loja).
    
    Demuestra el funcionamiento del sistema con una ruta fija
    que sirve como ejemplo de la funcionalidad.
    
    Returns:
        Response: Página con la ruta de ejemplo calculada
    """
    return GrafoController.ver_camino_fijo()

@starter_bp.route('/grafo_imagen')
@login_required
def grafo_imagen():
    """
    Genera y retorna imagen del grafo completo del sistema.
    
    Crea una visualización de todas las ciudades y sus conexiones
    usando NetworkX y Matplotlib.
    
    Returns:
        Response: Imagen PNG del grafo completo
    """
    return GrafoController.generar_imagen_grafo()

@starter_bp.route('/grafo_imagen_camino')
@login_required
def grafo_imagen_camino():
    """
    Genera imagen del grafo con un camino específico resaltado.
    
    Recibe parámetros de URL con las ciudades del camino
    y las resalta sobre el grafo completo.
    
    Returns:
        Response: Imagen PNG del grafo con camino resaltado
    """
    return GrafoController.generar_imagen_camino()

@starter_bp.route('/exportar_pdf')
@login_required
def exportar_pdf():
    """
    Exporta los detalles de una ruta calculada a PDF.
    
    Genera un documento PDF completo con información de la ruta,
    estadísticas, tabla paso a paso e imagen del grafo.
    
    Returns:
        Response: Archivo PDF para descarga
    """
    return GrafoController.exportar_ruta_pdf()
