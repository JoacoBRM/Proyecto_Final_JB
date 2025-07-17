// Validaciones y funcionalidad para la administración de rutas

// Validar que origen y destino sean diferentes
document.addEventListener('DOMContentLoaded', function() {
    const addRutaForm = document.getElementById('addRutaForm');
    
    if (addRutaForm) {
        addRutaForm.addEventListener('submit', function(e) {
            const origen = document.getElementById('ciudad_origen').value;
            const destino = document.getElementById('ciudad_destino').value;
            const costo = document.getElementById('costo').value;
            
            // Validar que origen y destino sean diferentes
            if (origen === destino) {
                e.preventDefault();
                alert('La ciudad de origen y destino deben ser diferentes');
                return false;
            }
            
            // Validar que se hayan seleccionado las ciudades
            if (!origen || !destino) {
                e.preventDefault();
                alert('Debe seleccionar tanto ciudad de origen como de destino');
                return false;
            }
            
            // Validar que el costo sea válido
            if (!costo || isNaN(costo) || parseFloat(costo) <= 0) {
                e.preventDefault();
                alert('El costo debe ser un número positivo');
                return false;
            }
        });
    }

    // Limpiar formulario cuando se cierre el modal
    const addRutaModal = document.getElementById('addRutaModal');
    if (addRutaModal) {
        $('#addRutaModal').on('hidden.bs.modal', function () {
            const form = document.getElementById('addRutaForm');
            if (form) {
                form.reset();
            }
        });
    }

    // Auto-cerrar alertas después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            $(alert).fadeOut('slow');
        });
    }, 5000);

    // Manejar modal de edición de ruta
    $('#editRutaModal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Botón que activó el modal
        const rutaId = button.data('ruta-id');
        const ciudadOrigen = button.data('ciudad-origen');
        const ciudadDestino = button.data('ciudad-destino');
        const costo = button.data('costo');
        
        const modal = $(this);
        modal.find('#edit_ruta_id').val(rutaId);
        modal.find('#edit_costo').val(costo);
    });

    // Validar formulario de edición
    const editRutaForm = document.getElementById('editRutaForm');
    if (editRutaForm) {
        editRutaForm.addEventListener('submit', function(e) {
            const costo = document.getElementById('edit_costo').value;
            
            // Validar que el costo sea válido
            if (!costo || isNaN(costo) || parseFloat(costo) <= 0) {
                e.preventDefault();
                alert('El costo debe ser un número positivo');
                return false;
            }
        });
    }

    // Limpiar formulario de edición cuando se cierre el modal
    $('#editRutaModal').on('hidden.bs.modal', function () {
        const form = document.getElementById('editRutaForm');
        if (form) {
            form.reset();
        }
    });
});

