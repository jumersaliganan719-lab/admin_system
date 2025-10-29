<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: ../login.php");
    exit;
}
include('../config/database.php');

// Handle Add Certificate
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['add_certificate'])) {
    $document_name = trim($_POST['document_name']);

    if (!empty($document_name)) {
        $stmt = $conn->prepare("INSERT INTO documents (document_name, status) VALUES (?, 'Available')");
        $stmt->bind_param("s", $document_name);
        $stmt->execute();
        $stmt->close();
    }
    header("Location: barangay_documents.php");
    exit;
}

// Handle Delete Certificate
if (isset($_GET['delete_id'])) {
    $delete_id = $_GET['delete_id'];
    $conn->query("DELETE FROM documents WHERE id = $delete_id");
    header("Location: barangay_documents.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Barangay Documents</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            width: 90%;
            margin: 30px auto;
        }
        h2 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
            background: #f8f8f8;
            padding: 15px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        input[type="text"] {
            padding: 8px;
            width: 300px;
            border: 1px solid #aaa;
            border-radius: 4px;
        }
        button {
            padding: 8px 15px;
            border: none;
            background: #007bff;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: center;
        }
        th {
            background: #007bff;
            color: white;
        }
        .generate-btn {
            background: #ffc107;
            color: black;
        }
        .generate-btn:hover {
            background: #e0a800;
        }
        .delete-btn {
            background: #dc3545;
            color: white;
        }
        .delete-btn:hover {
            background: #b52b37;
        }
    </style>
</head>
<body>
<div class="nav">
    <a href="dashboard.php">Dashboard</a>
    <a href="residents.php">Residents</a>
    <a href="barangay_documents.php">Documents</a>
    <a href="logout.php">Logout</a>
</div>

<div class="container">
    <h2>📄 Barangay Documents Management</h2>

    <!-- Add New Certificate Form -->
    <form method="POST">
        <label for="document_name"><strong>Add New Certificate:</strong></label>
        <input type="text" name="document_name" id="document_name" placeholder="Enter certificate name" required>
        <button type="submit" name="add_certificate">➕ Add</button>
    </form>

    <!-- Certificates Table -->
    <table>
        <tr>
            <th>ID</th>
            <th>Document Name</th>
            <th>Purpose</th>
            <th>Requestee Type</th>
            <th>Date Requested</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
        <?php
        $res = $conn->query("SELECT * FROM documents ORDER BY id ASC");
        if ($res && $res->num_rows > 0) {
            while ($row = $res->fetch_assoc()) {
                echo "<tr>
                        <td>{$row['id']}</td>
                        <td>{$row['document_name']}</td>
                        <td>" . ($row['purpose'] ?? '-') . "</td>
                        <td>" . ($row['requestee_type'] ?? '-') . "</td>
                        <td>" . ($row['date_requested'] ?? '-') . "</td>
                        <td>" . ($row['status'] ?? '-') . "</td>
                        <td>
                            <a href='certificate_preview.php?id={$row['id']}' target='_blank'>
                                <button type='button' class='generate-btn'>Generate</button>
                            </a>
                            <a href='barangay_documents.php?delete_id={$row['id']}' onclick=\"return confirm('Are you sure you want to delete this document?');\">
                                <button type='button' class='delete-btn'>Delete</button>
                            </a>
                        </td>
                      </tr>";
            }
        } else {
            echo "<tr><td colspan='7'>No certificates found.</td></tr>";
        }
        ?>
    </table>
</div>
</body>
</html>
