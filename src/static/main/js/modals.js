/* ========================================
   SISTEMA DE MODALES Y ALERTAS PERSONALIZADAS
   ======================================== */

class CustomAlerts {
    constructor() {
        this.toastContainer = null;
        this.init();
    }

    init() {
        // Crear contenedor de toasts si no existe
        if (!document.querySelector('.toast-container')) {
            this.toastContainer = document.createElement('div');
            this.toastContainer.className = 'toast-container';
            document.body.appendChild(this.toastContainer);
        } else {
            this.toastContainer = document.querySelector('.toast-container');
        }
    }

    // Modal de confirmación personalizado
    confirm(options) {
        return new Promise((resolve) => {
            const {
                title = '¿Confirmar acción?',
                message = '¿Está seguro de que desea continuar?',
                confirmText = 'Confirmar',
                cancelText = 'Cancelar',
                type = 'warning',
                confirmButtonClass = 'modal-btn-danger'
            } = options;

            // Crear el modal
            const modalHtml = `
                <div class="modal-overlay" id="customConfirmModal">
                    <div class="custom-modal">
                        <div class="modal-header">
                            <div class="modal-icon ${type}">
                                <i class="fas fa-${this.getIconByType(type)}"></i>
                            </div>
                        </div>
                        <div class="modal-body">
                            <p class="modal-message">${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button class="modal-btn modal-btn-secondary" id="cancelBtn">
                                ${cancelText}
                            </button>
                            <button class="modal-btn ${confirmButtonClass}" id="confirmBtn">
                                ${confirmText}
                            </button>
                        </div>
                    </div>
                </div>
            `;

            // Insertar el modal en el DOM
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = document.getElementById('customConfirmModal');

            // Mostrar el modal
            setTimeout(() => modal.classList.add('show'), 10);

            // Event listeners
            const confirmBtn = document.getElementById('confirmBtn');
            const cancelBtn = document.getElementById('cancelBtn');

            const closeModal = (result) => {
                modal.classList.remove('show');
                setTimeout(() => {
                    modal.remove();
                    resolve(result);
                }, 300);
            };

            confirmBtn.addEventListener('click', () => closeModal(true));
            cancelBtn.addEventListener('click', () => closeModal(false));

            // Cerrar con ESC
            const handleEsc = (e) => {
                if (e.key === 'Escape') {
                    document.removeEventListener('keydown', handleEsc);
                    closeModal(false);
                }
            };
            document.addEventListener('keydown', handleEsc);

            // Cerrar al hacer clic fuera del modal
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    closeModal(false);
                }
            });
        });
    }

    // Modal de alerta simple
    alert(options) {
        return new Promise((resolve) => {
            const {
                title = 'Información',
                message = '',
                buttonText = 'Entendido',
                type = 'info'
            } = options;

            const modalHtml = `
                <div class="modal-overlay" id="customAlertModal">
                    <div class="custom-modal">
                        <div class="modal-header">
                            <div class="modal-icon ${type}">
                                <i class="fas fa-${this.getIconByType(type)}"></i>
                            </div>
                        </div>
                        <div class="modal-body">
                            <p class="modal-message">${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button class="modal-btn modal-btn-primary" id="alertOkBtn">
                                ${buttonText}
                            </button>
                        </div>
                    </div>
                </div>
            `;

            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = document.getElementById('customAlertModal');

            setTimeout(() => modal.classList.add('show'), 10);

            const closeModal = () => {
                modal.classList.remove('show');
                setTimeout(() => {
                    modal.remove();
                    resolve();
                }, 300);
            };

            document.getElementById('alertOkBtn').addEventListener('click', closeModal);

            // Cerrar con ESC
            const handleEsc = (e) => {
                if (e.key === 'Escape') {
                    document.removeEventListener('keydown', handleEsc);
                    closeModal();
                }
            };
            document.addEventListener('keydown', handleEsc);
        });
    }

    // Toast notifications
    toast(options) {
        const {
            title = '',
            message = '',
            type = 'info',
            duration = 5000,
            closable = true
        } = options;

        const toastId = 'toast_' + Date.now();
        const toastHtml = `
            <div class="toast ${type}" id="${toastId}">
                <div class="toast-icon">
                    <i class="fas fa-${this.getIconByType(type)}"></i>
                </div>
                <div class="toast-content">
                    ${title ? `<div class="toast-title">${title}</div>` : ''}
                    <div class="toast-message">${message}</div>
                </div>
                ${closable ? '<button class="toast-close" aria-label="Cerrar">&times;</button>' : ''}
            </div>
        `;

        this.toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toast = document.getElementById(toastId);

        // Mostrar el toast
        setTimeout(() => toast.classList.add('show'), 10);

        // Cerrar automáticamente
        if (duration > 0) {
            setTimeout(() => this.removeToast(toast), duration);
        }

        // Botón de cerrar
        if (closable) {
            const closeBtn = toast.querySelector('.toast-close');
            closeBtn.addEventListener('click', () => this.removeToast(toast));
        }

        return toast;
    }

    // Remover toast
    removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    // Obtener icono según el tipo
    getIconByType(type) {
        const icons = {
            'success': 'check',
            'error': 'times',
            'warning': 'exclamation-triangle',
            'info': 'info-circle',
            'danger': 'exclamation-triangle'
        };
        return icons[type] || 'info-circle';
    }

    // Modal de loading
    showLoading(message = 'Cargando...') {
        const modalHtml = `
            <div class="modal-overlay" id="loadingModal">
                <div class="custom-modal" style="max-width: 300px;">
                    <div class="modal-body" style="text-align: center; padding: 40px 24px;">
                        <div class="modal-loading"></div>
                        <span>${message}</span>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = document.getElementById('loadingModal');
        setTimeout(() => modal.classList.add('show'), 10);

        return modal;
    }

    // Cerrar modal de loading
    hideLoading() {
        const modal = document.getElementById('loadingModal');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        }
    }
}

// Instancia global
const customAlerts = new CustomAlerts();

// Funciones globales para facilitar el uso
window.showConfirm = (options) => customAlerts.confirm(options);
window.showAlert = (options) => customAlerts.alert(options);
window.showToast = (options) => customAlerts.toast(options);
window.showLoading = (message) => customAlerts.showLoading(message);
window.hideLoading = () => customAlerts.hideLoading();

// Sobrescribir confirm y alert nativos (opcional)
window.confirmNative = window.confirm;
window.alertNative = window.alert;

// Reemplazar las funciones nativas con las personalizadas
// Nota: No sobrescribimos confirm() para evitar conflictos con onclick
// window.confirm se mantiene nativo para compatibilidad

window.alert = function(message) {
    return customAlerts.alert({
        message: message,
        title: 'Información',
        type: 'info'
    });
};

// Exportar para uso modular
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CustomAlerts;
}
