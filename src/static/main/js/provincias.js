// Validaciones y funcionalidad para la administración de provincias

function validateTextInput(input) {
    // Remover cualquier caracter que no sea letra o espacio
    input.value = input.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]/g, '');
    
    // Remover espacios múltiples
    input.value = input.value.replace(/\s{2,}/g, ' ');
    
    // Remover espacios al inicio
    if (input.value.startsWith(' ')) {
        input.value = input.value.trimStart();
    }
}

// Configurar validaciones cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Validar formulario antes de enviar
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const nombreInput = document.getElementById('nombre');
            if (nombreInput) {
                const nombre = nombreInput.value.trim();
                
                if (nombre === '') {
                    e.preventDefault();
                    alert('El nombre de la provincia es obligatorio');
                    nombreInput.focus();
                    return false;
                }
                
                if (!/^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$/.test(nombre)) {
                    e.preventDefault();
                    alert('El nombre solo puede contener letras y espacios');
                    nombreInput.focus();
                    return false;
                }
                
                // Limpiar espacios adicionales antes de enviar
                nombreInput.value = nombre;
            }
        });
    }
});
