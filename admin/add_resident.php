<?php
include('../config/database.php');

$fullname = $_POST['fullname'];
$address = $_POST['address'];
$birthdate = $_POST['birthdate'];
$contact = $_POST['contact'];
$occupation = $_POST['occupation'];
$gender = $_POST['gender'];
$category = $_POST['category'];

$sql = "INSERT INTO residents (fullname, address, birthdate, contact, occupation, gender, category)
        VALUES ('$fullname', '$address', '$birthdate', '$contact', '$occupation', '$gender', '$category')";

if ($conn->query($sql) === TRUE) {
    echo "<script>alert('Resident added successfully'); window.location='residents.php';</script>";
} else {
    echo "Error: " . $conn->error;
}
?>
