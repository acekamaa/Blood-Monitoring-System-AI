// Load Chart Data on Page Load
document.addEventListener('DOMContentLoaded', () => {
    fetchBloodData();
});

// Form Submission
document.getElementById('bloodForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const bloodType = document.getElementById('bloodType').value;
    const county = document.getElementById('county').value;
    const date = document.getElementById('date').value;

    const data = { bloodType, county, date };

    fetch('http://localhost:5000/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = result.message;
        messageDiv.style.color = result.message.includes('success') ? '#27ae60' : '#e74c3c';
        if (result.message.includes('success')) {
            fetchBloodData(); // Refresh chart after successful submission
            document.getElementById('bloodForm').reset();
        }
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error: ' + error;
    });
});

// Fetch and Render Blood Type Data
function fetchBloodData() {
    fetch('http://localhost:5000/api/blood-types')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => item.blood_type);
            const counts = data.map(item => item.count);

            const ctx = document.getElementById('bloodChart').getContext('2d');
            
            // Destroy existing chart if it exists to avoid overlap
            if (window.bloodChart && typeof window.bloodChart.destroy === 'function') {
                window.bloodChart.destroy();
            }

            window.bloodChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: counts,
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                            '#9966FF', '#FF9F40', '#C9CBCF', '#E7E9ED'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Blood Type Distribution' }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}