<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: ../login.php");
    exit;
}
include('../config/database.php');
?>
<!DOCTYPE html>
<html>
<head>
    <title>Residents</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div class="nav">
    <a href="dashboard.php">Dashboard</a>
    <a href="residents.php">Residents</a>
    <a href="documents.php">Documents</a>
    <a href="logout.php">Logout</a>
</div>

<div class="container">
    <h2>👥 Residents</h2>

    <form method="POST" action="add_resident.php">
        <label>Full Name</label>
        <input type="text" name="fullname" required>

        <label>Address</label>
        <input type="text" name="address" required>

        <label>Birthdate</label>
        <input type="date" name="birthdate">

        <label>Contact</label>
        <input type="text" name="contact">

        <label>Occupation</label>
        <input type="text" name="occupation">

        <label>Gender</label>
        <select name="gender">
            <option>Male</option>
            <option>Female</option>
        </select>

        <label>Category</label>
        <select name="category">
            <option>Student</option>
            <option>Senior Citizen</option>
            <option>Government Employee</option>
            <option>Private Employee</option>
            <option>Person with Disability</option>
            <option>Others</option>
        </select>

        <button type="submit">Add Resident</button>
    </form>

    <h3>Registered Residents</h3>
    <table border="1" cellpadding="8" width="100%">
        <tr><th>ID</th><th>Name</th><th>Address</th><th>Category</th></tr>
        <?php
        $res = $conn->query("SELECT * FROM residents");
        while ($row = $res->fetch_assoc()) {
            echo "<tr><td>{$row['id']}</td><td>{$row['fullname']}</td><td>{$row['address']}</td><td>{$row['category']}</td></tr>";
        }
        ?>
    </table>
</div>
</body>
</html>
