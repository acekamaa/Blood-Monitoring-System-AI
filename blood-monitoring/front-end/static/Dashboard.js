document.addEventListener("DOMContentLoaded", async function () {
    const API_BASE_URL = "http://127.0.0.1:5000";

    // Fetch blood type distribution data
    try {
        const response = await fetch(`${API_BASE_URL}/blood-distribution`);
        const data = await response.json();
        
        const ctx = document.getElementById('bloodChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data.distribution),
                datasets: [{
                    label: 'Blood Units',
                    data: Object.values(data.distribution),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            }
        });
    } catch (error) {
        console.error("Error fetching blood distribution data:", error);
    }

    // Fetch shortage prediction
    try {
        const response = await fetch(`${API_BASE_URL}/predict-shortage`);
        const prediction = await response.json();
        document.getElementById("predictionText").innerText = `Prediction: ${prediction.prediction}`;
    } catch (error) {
        console.error("Error fetching prediction:", error);
    }

    // Handle report download
    document.getElementById("downloadReport").addEventListener("click", function () {
        window.location.href = `${API_BASE_URL}/download-report`;
    });
});
