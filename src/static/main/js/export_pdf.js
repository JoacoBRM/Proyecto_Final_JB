/**
 * Funcionalidad para exportar rutas a PDF
 */

document.addEventListener('DOMContentLoaded', function() {
    // Función para manejar la exportación a PDF
    function exportarRutaPDF(origen, destino) {
        // Mostrar indicador de carga
        const btn = event.target;
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando PDF...';
        btn.disabled = true;
        
        // Construir la URL para la exportación
        const url = `/grafos/exportar_pdf?origen=${encodeURIComponent(origen)}&destino=${encodeURIComponent(destino)}`;
        
        // Abrir en nueva ventana para descargar
        const link = document.createElement('a');
        link.href = url;
        link.target = '_blank';
        link.download = `ruta_${origen}_${destino}_${new Date().getTime()}.pdf`;
        
        // Simular click en el enlace
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Restaurar el botón después de un momento
        setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.disabled = false;
        }, 2000);
    }
    
    // Agregar event listeners a todos los botones de exportar PDF
    const exportButtons = document.querySelectorAll('.btn-export-pdf');
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const origen = this.dataset.origen;
            const destino = this.dataset.destino;
            
            if (origen && destino) {
                exportarRutaPDF(origen, destino);
            } else {
                alert('Error: No se pueden obtener los datos de origen y destino');
            }
        });
    });
});

// Función global para exportar PDF (para uso desde HTML inline)
function exportarPDF(origen, destino, btnElement) {
    if (!origen || !destino) {
        alert('Error: Faltan datos de origen y destino');
        return;
    }
    
    // Mostrar indicador de carga
    const originalContent = btnElement.innerHTML;
    btnElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando PDF...';
    btnElement.disabled = true;
    
    // Construir la URL para la exportación
    const url = `/grafos/exportar_pdf?origen=${encodeURIComponent(origen)}&destino=${encodeURIComponent(destino)}`;
    
    // Crear enlace temporal para descargar
    const link = document.createElement('a');
    link.href = url;
    link.target = '_blank';
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Restaurar el botón
    setTimeout(() => {
        btnElement.innerHTML = originalContent;
        btnElement.disabled = false;
    }, 2000);
}
