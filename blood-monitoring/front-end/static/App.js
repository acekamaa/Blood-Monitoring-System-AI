document.addEventListener("DOMContentLoaded", function () {
    const API_BASE_URL = "http://127.0.0.1:5000";
    
    // Handle file upload validation
    const fileInput = document.querySelector("input[type='file']");
    fileInput?.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const fileType = file.name.split(".").pop().toLowerCase();
            if (fileType !== "csv") {
                alert("Please upload a valid CSV file.");
                this.value = "";
            }
        }
    });
    
    // Handle CSV Upload
    uploadForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        const formData = new FormData(uploadForm);
        
        try {
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: "POST",
                body: formData
            });
            
            const result = await response.json();
            alert(result.message);
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("Failed to upload file. Please try again.");
        }
    });
    
    // Handle Feedback Form Submission
    feedbackForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        const formData = new FormData(feedbackForm);
        const jsonData = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch(`${API_BASE_URL}/feedback`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(jsonData)
            });
            
            const result = await response.json();
            alert(result.message);
            feedbackForm.reset();
        } catch (error) {
            console.error("Error submitting feedback:", error);
            alert("Failed to submit feedback. Please try again.");
        }
    });

    // Handle User Login
    document.getElementById("loginForm")?.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        const formData = new FormData(this);
        const jsonData = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(jsonData)
            });
            
            const result = await response.json();
            if (result.success) {
                window.location.href = "home.html";
            } else {
                alert("Login failed: " + result.message);
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("Failed to login. Please try again.");
        }
    });

    // Predict Shortage
    document.getElementById("predictShortage")?.addEventListener("click", async function () {
        try {
            const response = await fetch(`${API_BASE_URL}/predict-shortage`);
            const result = await response.json();
            alert("Prediction: " + result.prediction);
        } catch (error) {
            console.error("Prediction error:", error);
            alert("Failed to predict shortage. Please try again.");
        }
    });

    // Check Blood Level
    document.getElementById("checkBloodLevel")?.addEventListener("click", async function () {
        try {
            const response = await fetch(`${API_BASE_URL}/check-blood-level`);
            const result = await response.json();
            alert("Blood Level: " + result.level);
        } catch (error) {
            console.error("Error checking blood level:", error);
            alert("Failed to check blood level. Please try again.");
        }
    });
});
