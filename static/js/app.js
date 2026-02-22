document.addEventListener('DOMContentLoaded', function () {
    // Check if we are on the vehicle detail page by looking for the chart data
    const chartDataElement = document.getElementById('chart-data');
    if (chartDataElement) {
        try {
            const chartData = JSON.parse(chartDataElement.textContent);

            const ctx = document.getElementById('socChart').getContext('2d');

            // Generate dynamic colors based on SoC value to visually show variations
            const bgColors = chartData.data.map(val => {
                if (val >= 80) return 'rgba(40, 167, 69, 0.6)'; // Green for High Charge
                if (val >= 30) return 'rgba(0, 123, 255, 0.6)'; // Blue for Medium Charge
                return 'rgba(220, 53, 69, 0.6)';                // Red for Low Charge
            });
            const borderColors = chartData.data.map(val => {
                if (val >= 80) return 'rgba(40, 167, 69, 1)';
                if (val >= 30) return 'rgba(0, 123, 255, 1)';
                return 'rgba(220, 53, 69, 1)';
            });

            // Draw simple Bar Chart using Chart.js
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'State of Charge (%)',
                        data: chartData.data,
                        backgroundColor: bgColors,
                        borderColor: borderColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'SoC (%)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Error setting up chart:", e);
        }
    }
});
