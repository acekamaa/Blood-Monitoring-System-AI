<?php
session_start();
include('db.php'); // Include your database connection file

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    $password2 = trim($_POST['password2']);
    $email = trim($_POST['email']);

    if (empty($username) || empty($password) || empty($password2) || empty($email)) {
        $_SESSION['error'] = 'All fields are required.';
        header('Location: signup.html');
        exit();
    }

    if ($password !== $password2) {
        $_SESSION['error'] = 'Passwords do not match.';
        header('Location: signup.html');
        exit();
    }

    // Check if username or email already exists
    $stmt = $conn->prepare('SELECT * FROM users WHERE username = ? OR email = ?');
    $stmt->bind_param('ss', $username, $email);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $_SESSION['error'] = 'Username or email already exists.';
        header('Location: signup.html');
        exit();
    }

    // Hash the password
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Insert the new user into the database
    $stmt = $conn->prepare('INSERT INTO users (username, email, password) VALUES (?, ?, ?)');
    $stmt->bind_param('sss', $username, $email, $hashed_password);

    if ($stmt->execute()) {
        $_SESSION['success'] = 'Signup successful!';
        header('Location: login.html');
    } else {
        $_SESSION['error'] = 'Signup failed. Please try again.';
        header('Location: signup.html');
    }
}
?>