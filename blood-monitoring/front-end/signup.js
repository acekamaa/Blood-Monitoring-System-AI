document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.signup-box form');
    const errorMessage = document.querySelector('.signup-box .error');
    const successMessage = document.querySelector('.signup-box .success');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password')
        };

        // Simulate form submission
        setTimeout(() => {
            if (data.username && data.email && data.password) {
                successMessage.textContent = 'Signup successful!';
                errorMessage.textContent = '';
            } else {
                errorMessage.textContent = 'Please fill in all fields.';
                successMessage.textContent = '';
            }
        }, 1000);
    });
});