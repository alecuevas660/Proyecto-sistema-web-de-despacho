document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('productForm');
    const nameInput = document.getElementById('id_name');
    const priceInput = document.getElementById('id_price');
    const stockMinInput = document.getElementById('id_stock_minimo');

    // Validación en tiempo real para el nombre
    nameInput.addEventListener('input', function() {
        validateField(this, {
            required: true,
            minLength: 3,
            pattern: /^[a-zA-Z0-9\s]*$/,
            messages: {
                required: 'El nombre es requerido',
                minLength: 'El nombre debe tener al menos 3 caracteres',
                pattern: 'El nombre solo puede contener letras, números y espacios'
            }
        });
    });

    // Validación en tiempo real para el precio
    priceInput.addEventListener('input', function() {
        const value = parseFloat(this.value);
        validateField(this, {
            required: true,
            min: 0,
            max: 999999.99,
            messages: {
                required: 'El precio es requerido',
                min: 'El precio debe ser mayor que 0',
                max: 'El precio no puede ser mayor a 999,999.99'
            }
        });
    });

    // Validación en tiempo real para el stock mínimo
    stockMinInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        validateField(this, {
            required: true,
            min: 0,
            max: 9999,
            messages: {
                required: 'El stock mínimo es requerido',
                min: 'El stock mínimo no puede ser negativo',
                max: 'El stock mínimo no puede ser mayor a 9,999'
            }
        });
    });

    // Funciones de validación
    function validateField(input, rules) {
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Validar requerido
        if (rules.required && !value) {
            isValid = false;
            errorMessage = rules.messages.required;
        }
        // Validar longitud mínima
        else if (rules.minLength && value.length < rules.minLength) {
            isValid = false;
            errorMessage = rules.messages.minLength;
        }
        // Validar patrón
        else if (rules.pattern && !rules.pattern.test(value)) {
            isValid = false;
            errorMessage = rules.messages.pattern;
        }
        // Validar mínimo y máximo para números
        else if (rules.min !== undefined || rules.max !== undefined) {
            const numValue = parseFloat(value);
            if (isNaN(numValue)) {
                isValid = false;
                errorMessage = 'Debe ser un número válido';
            } else if (rules.min !== undefined && numValue <= rules.min) {
                isValid = false;
                errorMessage = rules.messages.min;
            } else if (rules.max !== undefined && numValue > rules.max) {
                isValid = false;
                errorMessage = rules.messages.max;
            }
        }

        updateFieldStatus(input, isValid, errorMessage);
        return isValid;
    }

    function updateFieldStatus(input, isValid, errorMessage = '') {
        input.classList.remove('is-valid', 'is-invalid');
        input.classList.add(isValid ? 'is-valid' : 'is-invalid');

        const errorDiv = input.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
            errorDiv.innerHTML = isValid ? '' : 
                `<p class="mb-0 text-danger">
                    <i class="fas fa-exclamation-circle"></i> ${errorMessage}
                </p>`;
            errorDiv.style.display = isValid ? 'none' : 'block';
        }
    }

    // Validación del formulario completo
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let isValid = true;
        const fields = form.querySelectorAll('input, select, textarea');
        
        fields.forEach(field => {
            if (field.hasAttribute('required') && !field.value.trim()) {
                isValid = false;
                updateFieldStatus(field, false, 'Este campo es requerido');
            }
        });

        if (isValid) {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
            submitBtn.disabled = true;
            form.submit();
        }
    });
}); 