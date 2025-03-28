<?php
session_start();
include('db.php'); // Include your database connection file

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    if (empty($username) || empty($password)) {
        $_SESSION['error'] = 'All fields are required.';
        header('Location: login.html');
        exit();
    }

    // Check if the user exists
    $stmt = $conn->prepare('SELECT * FROM users WHERE username = ?');
    $stmt->bind_param('s', $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 0) {
        $_SESSION['error'] = 'Invalid username or password.';
        header('Location: login.html');
        exit();
    }

    $user = $result->fetch_assoc();

    // Verify the password
    if (password_verify($password, $user['password'])) {
        $_SESSION['username'] = $user['username'];
        header('Location: dashboard.html'); // Redirect to the dashboard or home page
    } else {
        $_SESSION['error'] = 'Invalid username or password.';
        header('Location: login.html');
    }
}
?>