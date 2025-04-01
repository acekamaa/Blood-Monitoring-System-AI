document.addEventListener("DOMContentLoaded", function () {
    const API_BASE_URL = "http://127.0.0.1:5000";

    // Handle Login
    document.getElementById("loginForm")?.addEventListener("submit", async function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        if (result.success) {
            window.location.href = "home.html"; // Redirect on success
        } else {
            alert("Login failed: " + result.message);
        }
    });

    // Handle File Upload
    document.getElementById("uploadBtn")?.addEventListener("click", async function () {
        const fileInput = document.getElementById("csvFile");
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        alert(result.message || result.error);
    });

    // Handle Prediction Fetching
    document.getElementById("predictShortage")?.addEventListener("click", async function () {
        const response = await fetch(`${API_BASE_URL}/predict-shortage`);
        const result = await response.json();
        document.getElementById("predictionText").innerText = `Prediction: ${result.prediction}`;
    });

    // Handle Blood Level Check
    document.getElementById("checkBloodLevel")?.addEventListener("click", async function () {
        const response = await fetch(`${API_BASE_URL}/check-blood-level`);
        const result = await response.json();
        document.getElementById("bloodLevelText").innerText = `Blood Level: ${result.level}`;
    });
});
