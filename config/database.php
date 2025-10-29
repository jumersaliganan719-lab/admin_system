<?php
// DATABASE CONNECTION SETTINGS
$servername = "localhost";   // your local server
$username = "root";           // default username for XAMPP
$password = "";               // leave empty (no password by default)
$dbname = "admin_system_db";  // name of your database in phpMyAdmin

// CREATE CONNECTION
$conn = new mysqli($servername, $username, $password, $dbname);

// CHECK CONNECTION
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
