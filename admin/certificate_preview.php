<?php
include('../config/database.php');

// Check if an ID is passed
if (!isset($_GET['id'])) {
    die("No document ID provided.");
}

$doc_id = intval($_GET['id']);

// Fetch document info
$doc_query = $conn->query("SELECT * FROM documents WHERE id = $doc_id");
if ($doc_query->num_rows == 0) {
    die("Document not found.");
}
$document = $doc_query->fetch_assoc();

// Fetch resident info
$resident_id = $document['resident_id'];
$res_query = $conn->query("SELECT * FROM residents WHERE id = $resident_id");
$resident = $res_query->fetch_assoc();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Certificate Preview - <?php echo htmlspecialchars($document['document_name']); ?></title>
    <style>
        body {
            font-family: "Times New Roman", serif;
            margin: 50px;
            background: #fff;
            color: #000;
        }
        .certificate {
            border: 3px solid #000;
            padding: 40px;
            text-align: center;
            width: 80%;
            margin: auto;
        }
        h1, h2, h3 {
            margin: 5px;
        }
        .details {
            text-align: left;
            margin-top: 30px;
            line-height: 1.8;
        }
        .center {
            text-align: center;
        }
        .print-btn {
            margin: 20px auto;
            display: block;
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 6px;
        }
        .print-btn:hover {
            background: #0056b3;
        }
        @media print {
            .print-btn { display: none; }
        }
    </style>
</head>
<body>
    <div class="certificate">
        <h2>Republic of the Philippines</h2>
        <h3>Province of [Your Province]</h3>
        <h3>Municipality of [Your Municipality]</h3>
        <h1><u><?php echo strtoupper($document['document_name']); ?></u></h1>
        <br><br>

        <div class="details">
            <p>TO WHOM IT MAY CONCERN:</p>
            <p>
                This is to certify that 
                <b><?php echo strtoupper($resident['fullname'] ?? 'Unknown Resident'); ?></b>,
                of legal age, residing at 
                <b><?php echo htmlspecialchars($resident['address'] ?? 'No address'); ?></b>, 
                is a bona fide resident of this Barangay.
            </p>

            <?php if (!empty($document['purpose'])): ?>
                <p>This certification is issued upon the request of the interested party for the purpose of 
                <b><?php echo htmlspecialchars($document['purpose']); ?></b>.</p>
            <?php endif; ?>

            <p>Issued this <?php echo date("jS \of F, Y"); ?> at Barangay [Barangay Name], [Municipality].</p>
        </div>

        <br><br>
        <div class="center">
            <p><b>______________________________</b><br>
            Barangay Captain</p>
        </div>
    </div>

    <button class="print-btn" onclick="window.print()">🖨️ Print Certificate</button>
</body>
</html>
