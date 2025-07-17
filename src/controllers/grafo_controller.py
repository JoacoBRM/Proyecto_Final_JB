"""
Controlador de Grafos
====================

Este módulo contiene la lógica de negocio para el manejo de grafos y
el cálculo de rutas óptimas usando el algoritmo de Dijkstra.

Funcionalidades principales:
- Cálculo de rutas óptimas entre ciudades
- Generación de visualizaciones del grafo
- Estadísticas del sistema de rutas
- Exportación de resultados a PDF

Autor: Joaquín Bermeo
Fecha: Julio 2025
"""

from flask import render_template, request, Response
from utils.grafo_db_utils import (
    grafo_a_imagen, 
    camino_optimo_con_costera, 
    obtener_ciudades, 
    grafo_a_imagen_camino,
    obtener_estadisticas_grafo,
    validar_ciudades_existen
)
from datetime import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class GrafoController:
    """
    Controlador que maneja toda la lógica relacionada con grafos y rutas.
    
    Este controlador implementa el patrón MVC separando la lógica de negocio
    de la presentación. Coordina entre los modelos de datos y las vistas.
    """
    
    @staticmethod
    def mostrar_introduccion():
        """
        Muestra la página de introducción con estadísticas del sistema de grafos.
        
        Returns:
            render_template: Página de introducción con estadísticas actualizadas
        """
        try:
            # Obtener estadísticas dinámicas desde la base de datos
            stats = obtener_estadisticas_grafo()
            stats['fecha_actualizacion'] = datetime.now().strftime('%d/%m/%Y')
            
            return render_template('grafos/starter.html', stats=stats)
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            # Fallback con datos básicos en caso de error de conexión
            stats = {
                'total_ciudades': 0,
                'ciudades_costeras': 0,
                'fecha_actualizacion': datetime.now().strftime('%d/%m/%Y'),
                'error': 'Error conectando con la base de datos'
            }
            return render_template('grafos/starter.html', stats=stats)
    
    @staticmethod
    def calcular_camino():
        """
        Maneja el cálculo de rutas óptimas entre ciudades seleccionadas por el usuario.
        
        Proceso:
        1. Obtiene lista de ciudades disponibles
        2. Valida datos de entrada del formulario
        3. Ejecuta algoritmo de Dijkstra
        4. Formatea y presenta resultados
        
        Returns:
            render_template: Página de cálculo con resultados o errores
        """
        try:
            # Obtener todas las ciudades disponibles para los selectores
            ciudades = obtener_ciudades()
        except Exception as e:
            print(f"Error obteniendo ciudades: {e}")
            return render_template(
                'grafos/calcular_camino.html', 
                ciudades=[], 
                error='Error conectando con la base de datos'
            )
        
        resultado = None
        
        if request.method == 'POST':
            # Obtener datos del formulario
            origen = request.form.get('origen')
            destino = request.form.get('destino')
            
            # Validación básica de datos de entrada
            if not origen or not destino:
                return render_template(
                    'grafos/calcular_camino.html', 
                    ciudades=ciudades, 
                    error='Por favor selecciona origen y destino'
                )
            
            # Validar que origen y destino sean diferentes
            if origen == destino:
                return render_template(
                    'grafos/calcular_camino.html', 
                    ciudades=ciudades, 
                    error='El origen y destino no pueden ser iguales'
                )
            
            # Validar que las ciudades existan en la base de datos
            valido, mensaje = validar_ciudades_existen(origen, destino)
            if not valido:
                return render_template(
                    'grafos/calcular_camino.html', 
                    ciudades=ciudades, 
                    error=mensaje
                )
            
            # Ejecutar algoritmo de Dijkstra para encontrar la ruta óptima
            try:
                resultado = camino_optimo_con_costera(origen, destino)
                
                # Enriquecer resultado con información adicional
                if resultado and resultado['camino']:
                    resultado['distancia_total'] = len(resultado['camino']) - 1  # Número de saltos
                    resultado['tiempo_estimado'] = resultado['costo'] * 2        # Estimación simplificada
                    resultado['fecha_calculo'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                    
                    # Información sobre ciudades costeras en la ruta
                    if resultado.get('ciudades_costeras_en_ruta'):
                        resultado['info_costeras'] = f"Pasa por las ciudades costeras: {', '.join(resultado['ciudades_costeras_en_ruta'])}"
                    else:
                        resultado['info_costeras'] = "Esta ruta no pasa por ciudades costeras"
                        
            except Exception as e:
                print(f"Error calculando ruta: {e}")
                return render_template(
                    'grafos/calcular_camino.html', 
                    ciudades=ciudades, 
                    error='Error calculando la ruta'
                )
        
        return render_template(
            'grafos/calcular_camino.html', 
            ciudades=ciudades, 
            resultado=resultado
        )
    
    @staticmethod
    def ver_camino_fijo():
        """
        Muestra una ruta predefinida del sistema (Ibarra - Loja).
        
        Esta función demuestra el funcionamiento del algoritmo con una ruta fija
        que sirve como ejemplo del sistema.
        
        Returns:
            render_template: Página con la ruta predefinida calculada
        """
        try:
            # Verificar que las ciudades de la ruta fija existan en la base de datos
            valido, mensaje = validar_ciudades_existen("Ibarra", "Loja")
            if not valido:
                return render_template('grafos/camino.html', 
                                    resultado={'error': mensaje})
            
            # Calcular la ruta óptima entre las ciudades fijas
            resultado = camino_optimo_con_costera("Ibarra", "Loja")
            
            # Enriquecer resultado con información adicional
            if resultado and resultado['camino']:
                resultado['distancia_total'] = len(resultado['camino']) - 1
                resultado['tiempo_estimado'] = resultado['costo'] * 2
                resultado['fecha_calculo'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                resultado['descripcion'] = "Ruta óptima predefinida del sistema"
                
                # Información sobre ciudades costeras en la ruta
                if resultado.get('ciudades_costeras_en_ruta'):
                    resultado['info_costeras'] = f"Pasa por las ciudades costeras: {', '.join(resultado['ciudades_costeras_en_ruta'])}"
                else:
                    resultado['info_costeras'] = "Esta ruta no pasa por ciudades costeras"
            
            return render_template('grafos/camino.html', resultado=resultado)
            
        except Exception as e:
            print(f"Error calculando ruta fija: {e}")
            return render_template('grafos/camino.html', 
                                resultado={'error': 'Error calculando la ruta desde la base de datos'})
    
    @staticmethod
    def generar_imagen_grafo():
        """
        Genera una imagen visual del grafo completo del sistema.
        
        Utiliza NetworkX y Matplotlib para crear una representación gráfica
        de todas las ciudades y sus conexiones.
        
        Returns:
            Response: Imagen PNG del grafo o error 500
        """
        try:
            buf = grafo_a_imagen()
            return Response(buf.getvalue(), mimetype='image/png')
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return Response("Error generando imagen", status=500)
    
    @staticmethod
    def generar_imagen_camino():
        """
        Genera una imagen del grafo con una ruta específica resaltada.
        
        Recibe una lista de ciudades que forman un camino y las resalta
        en color diferente sobre el grafo completo.
        
        Args (via URL parameters):
            camino (list): Lista de nombres de ciudades que forman la ruta
            
        Returns:
            Response: Imagen PNG del grafo con camino resaltado o error 500
        """
        try:
            # Obtener el camino desde los parámetros de la URL
            camino = request.args.getlist('camino')
            buf = grafo_a_imagen_camino(camino)
            return Response(buf.getvalue(), mimetype='image/png')
        except Exception as e:
            print(f"Error generando imagen con camino: {e}")
            return Response("Error generando imagen", status=500)
    
    @staticmethod
    def get_estadisticas_grafo():
        """
        Obtiene estadísticas actualizadas del grafo desde la base de datos.
        
        Calcula métricas como número total de ciudades, ciudades costeras,
        rutas disponibles y promedios de costos.
        
        Returns:
            dict: Diccionario con estadísticas del grafo o información de error
        """
        try:
            return obtener_estadisticas_grafo()
        except Exception as e:
            print(f"Error obteniendo estadísticas del grafo: {e}")
            return {
                'total_ciudades': 0,
                'ciudades_costeras': 0,
                'total_rutas': 0,
                'rutas_posibles': 0,
                'costo_promedio': 0,
                'ciudades': [],
                'error': 'Error conectando con la base de datos'
            }

    @staticmethod
    def exportar_ruta_pdf():
        """
        Genera un archivo PDF con los detalles completos de una ruta calculada.
        
        El PDF incluye:
        - Información de origen y destino
        - Ruta completa paso a paso
        - Costo total y tiempo estimado
        - Fecha de generación
        - Estadísticas adicionales
        
        Args (via URL parameters):
            origen (str): Ciudad de origen
            destino (str): Ciudad de destino
            
        Returns:
            Response: Archivo PDF descargable o mensaje de error
        """
        try:
            # Obtener parámetros de la URL
            origen = request.args.get('origen')
            destino = request.args.get('destino')
            
            # Validar que se proporcionen ambos parámetros
            if not origen or not destino:
                return Response("Faltan parámetros origen y destino", status=400)
            
            # Calcular la ruta usando el algoritmo de Dijkstra
            resultado = camino_optimo_con_costera(origen, destino)
            
            # Verificar que se haya encontrado una ruta válida
            if not resultado or not resultado.get('camino'):
                return Response("No se pudo calcular la ruta", status=404)
            
            # Crear el documento PDF en memoria usando ReportLab
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []  # Lista de elementos que formarán el contenido del PDF
            
            # Definir estilos personalizados para el documento
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue
            )
            
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=15,
                alignment=TA_LEFT,
                textColor=colors.darkgreen
            )
            
            normal_style = styles['Normal']
            normal_style.fontSize = 12
            normal_style.spaceAfter = 10
            
            # Agregar título y encabezado del documento
            story.append(Paragraph("Sistema de Análisis de Grafos", title_style))
            story.append(Paragraph("Reporte de Ruta Óptima", subtitle_style))
            story.append(Spacer(1, 20))
            
            # Información general del cálculo
            fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
            story.append(Paragraph(f"<b>Fecha de generación:</b> {fecha_actual}", normal_style))
            story.append(Paragraph(f"<b>Origen:</b> {origen}", normal_style))
            story.append(Paragraph(f"<b>Destino:</b> {destino}", normal_style))
            story.append(Spacer(1, 20))
            
            # Sección con detalles de la ruta calculada
            story.append(Paragraph("Detalles de la Ruta Calculada", subtitle_style))
            
            # Mostrar la ruta completa como una cadena de ciudades
            ruta_texto = " → ".join(resultado['camino'])
            story.append(Paragraph(f"<b>Ruta óptima:</b> {ruta_texto}", normal_style))
            story.append(Paragraph(f"<b>Costo total:</b> ${resultado['costo']:.2f}", normal_style))
            
            # Calcular y mostrar estadísticas adicionales
            paradas = len(resultado['camino']) - 1
            story.append(Paragraph(f"<b>Número de paradas:</b> {paradas} conexiones", normal_style))
            
            tiempo_estimado = resultado['costo'] * 2  # Estimación simple
            story.append(Paragraph(f"<b>Tiempo estimado:</b> {tiempo_estimado:.1f} horas", normal_style))
            
            # Información sobre validación de ciudades costeras
            if resultado.get('valido'):
                story.append(Paragraph("--> <b>Esta ruta pasa por al menos una ciudad costera</b>", normal_style))
            else:
                story.append(Paragraph("--> <b>Esta ruta NO pasa por ciudades costeras</b>", normal_style))
                
            story.append(Spacer(1, 30))
            
            # Crear tabla con detalles paso a paso de la ruta
            story.append(Paragraph("Detalles Paso a Paso", subtitle_style))
            
            # Preparar datos para la tabla
            table_data = [['Paso', 'Desde', 'Hacia', 'Observaciones']]
            
            # Llenar la tabla con cada segmento de la ruta
            for i in range(len(resultado['camino']) - 1):
                paso = i + 1
                desde = resultado['camino'][i]
                hacia = resultado['camino'][i + 1]
                obs = "Conexión directa"
                table_data.append([str(paso), desde, hacia, obs])
            
            # Crear y estilizar la tabla
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),        # Fondo gris para encabezado
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),   # Texto blanco en encabezado
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Centrar todo el texto
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),     # Fuente bold para encabezado
                ('FONTSIZE', (0, 0), (-1, 0), 12),                   # Tamaño de fuente del encabezado
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),              # Padding inferior del encabezado
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),      # Fondo beige para filas de datos
                ('GRID', (0, 0), (-1, -1), 1, colors.black)          # Bordes negros
            ]))
            
            story.append(table)
            story.append(Spacer(1, 30))
            
            # Intentar agregar imagen del grafo con la ruta resaltada
            try:
                # Generar imagen del grafo con la ruta resaltada
                img_buffer = grafo_a_imagen_camino(resultado['camino'])
                img_buffer.seek(0)
                
                # Crear objeto Image para el PDF con dimensiones específicas
                img = Image(img_buffer, width=400, height=300)
                img.hAlign = 'CENTER'
                
                story.append(Paragraph("Visualización del Grafo", subtitle_style))
                story.append(img)
                story.append(Paragraph("Grafo con la ruta óptima resaltada", normal_style))
                
            except Exception as e:
                print(f"Error agregando imagen al PDF: {e}")
                story.append(Paragraph("Error: No se pudo generar la imagen del grafo", normal_style))
            
            story.append(Spacer(1, 20))
            
            # Agregar información adicional sobre el sistema
            story.append(Paragraph("Información del Sistema", subtitle_style))
            story.append(Paragraph("Este reporte fue generado por el Sistema de Análisis de Grafos y Rutas Óptimas. Realizado por: Joaquin Bermeo.", normal_style))
            story.append(Paragraph("Algoritmo utilizado: Dijkstra para encontrar el camino más corto.", normal_style))
            story.append(Paragraph("Los costos están expresados en unidades monetarias.", normal_style))
            
            # Construir el PDF con todos los elementos
            doc.build(story)
            
            # Preparar la respuesta HTTP con el PDF
            buffer.seek(0)
            filename = f"ruta_{origen}_{destino}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            return Response(
                buffer.getvalue(),
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'application/pdf'
                }
            )
            
        except Exception as e:
            print(f"Error generando PDF: {e}")
            return Response(f"Error generando PDF: {str(e)}", status=500)
