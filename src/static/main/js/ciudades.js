// Validaciones y funcionalidad para la administración de ciudades

function agregarRuta() {
    const container = document.getElementById('rutasContainer');
    const rutaItem = container.querySelector('.ruta-item').cloneNode(true);
    
    // Limpiar valores
    rutaItem.querySelector('select').value = '';
    rutaItem.querySelector('input').value = '';
    
    container.appendChild(rutaItem);
}

function eliminarRuta(button) {
    const container = document.getElementById('rutasContainer');
    const rutaItems = container.querySelectorAll('.ruta-item');
    
    if (rutaItems.length > 1) {
        button.closest('.ruta-item').remove();
    }
}

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
    const formCrearCiudad = document.getElementById('formCrearCiudad');
    if (formCrearCiudad) {
        formCrearCiudad.addEventListener('submit', function(e) {
            const nombreInput = document.getElementById('nombre');
            if (nombreInput) {
                const nombre = nombreInput.value.trim();
                
                if (nombre === '') {
                    e.preventDefault();
                    alert('El nombre de la ciudad es obligatorio');
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
