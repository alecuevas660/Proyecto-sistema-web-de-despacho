document.addEventListener('DOMContentLoaded', function() {
    // Configuración de gráficos
    const ventasCtx = document.getElementById('ventasChart').getContext('2d');
    const productosCtx = document.getElementById('productosChart').getContext('2d');

    // Gráfico de Ventas Mensuales
    const ventasChart = new Chart(ventasCtx, {
        type: 'line',
        data: {
            labels: ventasLabels,
            datasets: [{
                label: 'Ventas',
                data: ventasData,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de Productos más Vendidos
    const productosChart = new Chart(productosCtx, {
        type: 'doughnut',
        data: {
            labels: productosLabels,
            datasets: [{
                data: productosData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
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