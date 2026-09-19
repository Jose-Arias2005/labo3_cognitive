document.addEventListener("DOMContentLoaded", () => {
    
    // Confirmación al eliminar usuario
    const formsEliminar = document.querySelectorAll('.form-eliminar');
    
    formsEliminar.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Confirmación simple
            if (confirm("¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.")) {
                this.submit();
            }
        });
    });

    // Auto-ocultar alertas flash después de 5 segundos
    const alertas = document.querySelectorAll('.alert');
    if(alertas.length > 0) {
        setTimeout(() => {
            alertas.forEach(alerta => {
                alerta.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                alerta.style.opacity = '0';
                alerta.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
});
