/* ========================================
    NOTIFICACIONES PARA OPERACIONES CRUD
======================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Mostrar notificaciones basadas en parámetros URL o mensajes flash
    checkForNotifications();
    
    // Interceptar formularios para mostrar loading
    setupFormSubmissionFeedback();
});

function checkForNotifications() {
    // Verificar parámetros URL para notificaciones
    const urlParams = new URLSearchParams(window.location.search);
    const successMessage = urlParams.get('success');
    const errorMessage = urlParams.get('error');
    
    if (successMessage) {
        showToast({
            title: '¡Operación exitosa!',
            message: decodeURIComponent(successMessage),
            type: 'success',
            duration: 4000
        });
        
        // Limpiar el parámetro de la URL
        urlParams.delete('success');
        const newUrl = window.location.pathname + (urlParams.toString() ? '?' + urlParams.toString() : '');
        window.history.replaceState({}, '', newUrl);
    }
    
    if (errorMessage) {
        showToast({
            title: 'Error',
            message: decodeURIComponent(errorMessage),
            type: 'error',
            duration: 6000
        });
        
        // Limpiar el parámetro de la URL
        urlParams.delete('error');
        const newUrl = window.location.pathname + (urlParams.toString() ? '?' + urlParams.toString() : '');
        window.history.replaceState({}, '', newUrl);
    }
    
    // También verificar mensajes flash de Flask
    checkFlashMessages();
}

function checkFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        let type = 'info';
        let title = 'Notificación';
        
        if (alert.classList.contains('alert-success')) {
            type = 'success';
            title = '¡Éxito!';
        } else if (alert.classList.contains('alert-danger')) {
            type = 'error';
            title = 'Error';
        } else if (alert.classList.contains('alert-warning')) {
            type = 'warning';
            title = 'Advertencia';
        }
        
        const message = alert.textContent.trim();
        if (message) {
            showToast({
                title: title,
                message: message,
                type: type,
                duration: 5000
            });
            
            // Ocultar la alerta original
            alert.style.display = 'none';
        }
    });
}

function setupFormSubmissionFeedback() {
    // Interceptar formularios de creación y edición
    const forms = document.querySelectorAll('form[action*="crear"], form[action*="editar"], form[action*="actualizar"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            
            if (submitBtn && !submitBtn.classList.contains('btn-delete')) {
                // Mostrar estado de carga en el botón
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="modal-loading"></span> Guardando...';
                submitBtn.disabled = true;
                
                // Restaurar el botón después de un tiempo (por si hay errores de validación)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

// Funciones específicas para diferentes tipos de operaciones
function showSuccessNotification(operation, itemName) {
    const messages = {
        'create': `${itemName} creado exitosamente`,
        'update': `${itemName} actualizado exitosamente`,
        'delete': `${itemName} eliminado exitosamente`
    };
    
    showToast({
        title: '¡Operación exitosa!',
        message: messages[operation] || 'Operación completada',
        type: 'success',
        duration: 4000
    });
}

function showErrorNotification(operation, error) {
    showToast({
        title: 'Error en la operación',
        message: error || 'Ocurrió un error inesperado',
        type: 'error',
        duration: 6000
    });
}

// Función para confirmar navegación si hay cambios sin guardar
function setupUnsavedChangesWarning() {
    const forms = document.querySelectorAll('form:not([data-no-warning])');
    let hasUnsavedChanges = false;
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                hasUnsavedChanges = true;
            });
        });
        
        form.addEventListener('submit', () => {
            hasUnsavedChanges = false;
        });
    });
    
    window.addEventListener('beforeunload', (e) => {
        if (hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = '¿Está seguro de que desea salir? Los cambios no guardados se perderán.';
            return e.returnValue;
        }
    });
}

// Función para validar formularios con feedback visual
function validateFormWithFeedback(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'Este campo es obligatorio');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validaciones específicas
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Por favor, ingrese un email válido');
            isValid = false;
        }
    });
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Exportar funciones para uso global
window.showSuccessNotification = showSuccessNotification;
window.showErrorNotification = showErrorNotification;
window.validateFormWithFeedback = validateFormWithFeedback;
