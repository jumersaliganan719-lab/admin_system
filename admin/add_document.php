<?php
include('../config/database.php');

$resident_id = $_POST['resident_id'];
$document_type = $_POST['document_type'];
$purpose = $_POST['purpose'];
$requestee_type = $_POST['requestee_type'];
$date_requested = date('Y-m-d');
$status = 'Pending';

$sql = "INSERT INTO documents (resident_id, document_type, purpose, requestee_type, date_requested, status)
        VALUES ('$resident_id', '$document_type', '$purpose', '$requestee_type', '$date_requested', '$status')";

if ($conn->query($sql) === TRUE) {
    echo "<script>alert('Document request added successfully'); window.location='documents.php';</script>";
} else {
    echo "Error: " . $conn->error;
}
?>
