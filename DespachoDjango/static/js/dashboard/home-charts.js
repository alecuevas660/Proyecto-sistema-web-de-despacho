document.addEventListener('DOMContentLoaded', function() {
    // Configuración de gráficos
    const ventasCtx = document.getElementById('ventasChart').getContext('2d');
    const productosCtx = document.getElementById('productosChart').getContext('2d');

    // Gráfico de ventas
    new Chart(ventasCtx, {
        type: 'line',
        data: {
            labels: ventasLabels, // Definido en el template
            datasets: [{
                label: 'Ventas',
                data: ventasData, // Definido en el template
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: true,
                backgroundColor: 'rgba(75, 192, 192, 0.1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de productos más vendidos
    new Chart(productosCtx, {
        type: 'doughnut',
        data: {
            labels: productosLabels, // Definido en el template
            datasets: [{
                data: productosData, // Definido en el template
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}); 