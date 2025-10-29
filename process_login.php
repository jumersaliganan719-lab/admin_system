<?php
session_start();
include('config/database.php');

$username = $_POST['username'];
$password = $_POST['password'];

// Simple validation (not yet hashed)
$sql = "SELECT * FROM admin WHERE username='$username' AND password='$password'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $_SESSION['admin'] = $username;
    header("Location: admin/dashboard.php");
    exit;
} else {
    header("Location: login.php?error=Invalid username or password");
    exit;
}
?>
