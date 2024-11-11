document.addEventListener('DOMContentLoaded', function() {
    const deleteModal = document.getElementById('deleteModal');
    const productNameSpan = document.getElementById('productName');
    const deleteForm = document.getElementById('deleteForm');

    deleteModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const productId = button.getAttribute('data-product-id');
        const productName = button.getAttribute('data-product-name');
        
        productNameSpan.textContent = productName;
        deleteForm.action = `/inventario/producto/${productId}/eliminar/`;
    });
}); 