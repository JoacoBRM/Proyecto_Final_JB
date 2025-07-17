/* ========================================
    SCRIPTS PARA ADMINISTRACIÓN
======================================== */

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    initializeAdminFeatures();
});

function initializeAdminFeatures() {
    // Auto-hide alerts
    setupAutoHideAlerts();
    
    // Form validations
    setupFormValidations();
    
    // Table enhancements
    setupTableEnhancements();
}

// Auto-ocultar alertas después de 5 segundos
function setupAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent):not(.modal .alert)');
    
    alerts.forEach(alert => {
        // Agregar animación de entrada
        alert.classList.add('fade-in-up');
        
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        }, 5000);
    });
}

// Validaciones de formularios
function setupFormValidations() {
    const forms = document.querySelectorAll('.admin-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                alert('Por favor, complete todos los campos obligatorios.');
            }
        });
    });
}

function validateForm(form) {
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
    
    return isValid;
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

// Mejoras para tablas
function setupTableEnhancements() {
    // Ordenamiento de tablas
    setupTableSorting();
    
    // Filtrado de tablas
    setupTableFiltering();
    
    // Selección múltiple
    setupTableSelection();
}

function setupTableSorting() {
    const sortableHeaders = document.querySelectorAll('th[data-sortable]');
    
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(this);
        });
        
        // Agregar icono de ordenamiento
        if (!header.querySelector('.sort-icon')) {
            const icon = document.createElement('i');
            icon.className = 'fas fa-sort sort-icon ml-1';
            header.appendChild(icon);
        }
    });
}

function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const isAscending = !header.classList.contains('sort-asc');
    
    // Limpiar iconos previos
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        const icon = th.querySelector('.sort-icon');
        if (icon) {
            icon.className = 'fas fa-sort sort-icon ml-1';
        }
    });
    
    // Ordenar filas
    rows.sort((a, b) => {
        const aText = a.children[columnIndex].textContent.trim();
        const bText = b.children[columnIndex].textContent.trim();
        
        const aValue = isNaN(aText) ? aText.toLowerCase() : parseFloat(aText);
        const bValue = isNaN(bText) ? bText.toLowerCase() : parseFloat(bText);
        
        if (isAscending) {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    // Actualizar tabla
    rows.forEach(row => tbody.appendChild(row));
    
    // Actualizar icono
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
    const icon = header.querySelector('.sort-icon');
    if (icon) {
        icon.className = `fas fa-sort-${isAscending ? 'up' : 'down'} sort-icon ml-1`;
    }
}

function setupTableFiltering() {
    const filterInputs = document.querySelectorAll('[data-filter-table]');
    
    filterInputs.forEach(input => {
        const tableId = input.dataset.filterTable;
        const table = document.getElementById(tableId);
        
        if (table) {
            input.addEventListener('input', function() {
                filterTable(table, this.value);
            });
        }
    });
}

function filterTable(table, searchTerm) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    const term = searchTerm.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
}

function setupTableSelection() {
    const selectAllCheckbox = document.querySelector('#selectAll');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    
    if (selectAllCheckbox && rowCheckboxes.length > 0) {
        selectAllCheckbox.addEventListener('change', function() {
            rowCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActions();
        });
        
        rowCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                updateSelectAll();
                updateBulkActions();
            });
        });
    }
}

function updateSelectAll() {
    const selectAllCheckbox = document.querySelector('#selectAll');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    const checkedBoxes = document.querySelectorAll('.row-checkbox:checked');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.checked = checkedBoxes.length === rowCheckboxes.length;
        selectAllCheckbox.indeterminate = checkedBoxes.length > 0 && checkedBoxes.length < rowCheckboxes.length;
    }
}

function updateBulkActions() {
    const bulkActions = document.querySelector('.bulk-actions');
    const checkedBoxes = document.querySelectorAll('.row-checkbox:checked');
    
    if (bulkActions) {
        bulkActions.style.display = checkedBoxes.length > 0 ? 'block' : 'none';
    }
}

// Funciones utilitarias
function showLoading(element) {
    element.classList.add('loading');
}

function hideLoading(element) {
    element.classList.remove('loading');
}

function showToast(message, type = 'info') {
    return window.showToast({
        message: message,
        type: type,
        duration: 4000
    });
}

// Exportar funciones para uso global
window.AdminUtils = {
    showLoading,
    hideLoading,
    showToast,
    validateForm,
    filterTable
};
