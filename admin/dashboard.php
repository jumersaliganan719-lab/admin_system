<?php 
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: ../login.php");
    exit;
}
include('../config/database.php');

// Query for chart data
$sql = "SELECT requestee_type, COUNT(*) as count FROM documents GROUP BY requestee_type";
$result = $conn->query($sql);

$types = [];
$counts = [];

while ($row = $result->fetch_assoc()) {
    $types[] = $row['requestee_type'];
    $counts[] = $row['count'];
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="../css/style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; }
        .nav a {
            text-decoration: none;
            margin-right: 15px;
            color: black;
            font-weight: bold;
        }
        .nav a:hover { color: blue; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #f4f4f4; }
        canvas { margin-top: 20px; }
    </style>
</head>
<body>

<div class="nav">
    <a href="dashboard.php" style="color:blue;">Dashboard</a>
    <a href="residents.php">Residents</a>
    <a href="documents.php">Documents</a>
    <a href="barangay_documents.php">Barangay Certificates</a> <!-- ✅ Added this -->
    <a href="logout.php">Logout</a>
</div>

<div class="container">
    <h2>📊 Request Summary by Type</h2>

    <table border="1" cellpadding="8" style="width:100%;">
        <tr><th>Requestee Type</th><th>Number of Requests</th></tr>
        <?php
        $result = $conn->query("SELECT requestee_type, COUNT(*) as count FROM documents GROUP BY requestee_type");
        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                echo "<tr><td>{$row['requestee_type']}</td><td>{$row['count']}</td></tr>";
            }
        } else {
            echo "<tr><td colspan='2'>No request data available.</td></tr>";
        }
        ?>
    </table>

    <canvas id="requestChart" width="400" height="200"></canvas>
</div>

<script>
const ctx = document.getElementById('requestChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: <?php echo json_encode($types); ?>,
        datasets: [{
            label: 'Number of Requests',
            data: <?php echo json_encode($counts); ?>,
            backgroundColor: [
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(199, 199, 199, 0.6)'
            ]
        }]
    },
    options: { scales: { y: { beginAtZero: true } } }
});
</script>

</body>
</html>
